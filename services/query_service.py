from datetime import datetime
from typing import List, Optional
from pymongo.collection import Collection
from core.database import MongoDBManager
from repository.sales_repository import SalesRepository
from core.logger import setup_logger
from time import perf_counter

logger = setup_logger(__name__)

class QueryService:
    def __init__(self, db_manager: MongoDBManager):
        self.db_manager = db_manager
        self.collection: Optional[Collection] = None
    
    def _ensure_collection(self) -> None:
        """Ensure we have a valid collection reference."""
        if not self.collection:
            self.collection = self.db_manager.get_collection(
                'app_seo_development',
                'itunes_sales_report_estimates'
            )
    
    def get_time_series(self, app_id: int, start_date: datetime, end_date: datetime) -> List[float]:
        """Get revenue time series for an app within date range."""
        start_time = perf_counter()
        try:
            self._ensure_collection()
            
            query = SalesRepository.build_time_series_query(app_id, start_date, end_date)
            projection = SalesRepository.get_projection()
            
            cursor = self.collection.find(query, projection).sort('d', 1)
            result = [doc['ir'] for doc in cursor]
            
            duration = perf_counter() - start_time
            logger.info(f"Query execution time: {duration:.2f} seconds")
            
            return result
        except Exception as e:
            logger.error(f"Failed to query time series: {e}")
            return [] 