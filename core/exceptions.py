class MongoDBError(Exception):
    """Base exception for MongoDB related errors."""
    pass

class DataRestorationError(MongoDBError):
    """Exception raised when data restoration fails."""
    pass

class ConnectionError(MongoDBError):
    """Exception raised when MongoDB connection fails."""
    pass

class ValidationError(MongoDBError):
    """Exception raised when data validation fails."""
    pass 