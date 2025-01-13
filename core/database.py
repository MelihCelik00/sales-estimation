from typing import Optional
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
from core.exceptions import ConnectionError
from core.logger import setup_logger

logger = setup_logger(__name__)

class MongoDBManager:
    def __init__(self, uri: str):
        self.uri = uri
        self.client: Optional[MongoClient] = None
    
    def __enter__(self) -> 'MongoDBManager':
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def connect(self) -> None:
        """Establish connection to MongoDB."""
        try:
            self.client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=5000,
                maxPoolSize=50,
                minPoolSize=10,
                maxIdleTimeMS=30000
            )
            self.client.server_info()  # Validate connection
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise ConnectionError(f"MongoDB connection failed: {e}")
    
    def close(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            self.client = None
    
    def get_collection(self, database: str, collection: str) -> Collection:
        """Get MongoDB collection."""
        if not self.client:
            self.connect()
        return self.client[database][collection] 