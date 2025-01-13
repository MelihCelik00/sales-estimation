import subprocess
import os
from typing import Optional
from pymongo.collection import Collection
from core.database import MongoDBManager
from core.exceptions import DataRestorationError
from repository.sales_repository import SalesRepository
from core.logger import setup_logger

logger = setup_logger(__name__)

class SetupService:
    def __init__(self, db_manager: MongoDBManager):
        self.db_manager = db_manager
        self.collection: Optional[Collection] = None
    
    def _ensure_collection(self) -> None:
        """Be sure that we have a valid collection reference."""
        if not self.collection:
            self.collection = self.db_manager.get_collection(
                'app_seo_development',
                'itunes_sales_report_estimates'
            )
    
    def restore_mongodb_dump(self) -> None:
        """Restore MongoDB database from dump files."""
        dump_path = os.path.join('mongo_dump')
        if not os.path.exists(dump_path):
            raise FileNotFoundError("mongo_dump directory missing")

        try:
            subprocess.run([
                'mongorestore',
                '--uri', self.db_manager.uri,
                '--drop',
                '--batchSize', '100000',
                '--numParallelCollections', '1',
                '--numInsertionWorkersPerCollection', '4',
                dump_path
            ], check=True, capture_output=True, text=True)
            logger.info("MongoDB dump restored successfully!")

        except subprocess.CalledProcessError as e:
            logger.error(f"mongorestore failed: {e.stdout}\n{e.stderr}")
            raise DataRestorationError("Failed to restore MongoDB dump")
    
    def verify_and_restore_data(self) -> bool:
        """Verify collection data and restore if needed."""
        self._ensure_collection()
        
        sample_data = self.collection.find_one({})
        if SalesRepository.verify_document(sample_data):
            return True

        logger.info("Data not properly restored. Running restore...")
        with self.db_manager.client.start_session() as session:
            session.start_transaction()
            try:
                self.collection.drop()
                self.restore_mongodb_dump()
                self._verify_restoration()
                self._create_indexes()
                session.commit_transaction()
                logger.info("Data restoration completed successfully!")
                return True
            except Exception as e:
                session.abort_transaction()
                logger.error(f"Data restoration failed: {e}")
                return False
    
    def _verify_restoration(self) -> None:
        """Verify that data restoration was successful."""
        new_sample = self.collection.find_one({})
        if not SalesRepository.verify_document(new_sample):
            raise DataRestorationError("Data restoration failed verification")
    
    def _create_indexes(self) -> None:
        """Create necessary indexes."""
        if 'aid_1_d_1' not in self.collection.index_information():
            logger.info("Creating index on (aid, d)...")
            self.collection.create_index([('aid', 1), ('d', 1)])
            logger.info("Index created successfully!") 