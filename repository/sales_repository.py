from datetime import datetime
from typing import Dict, Any, List

class SalesRepository:
    REQUIRED_FIELDS = {'aid', 'd', 'ir', 'cc'}

    @staticmethod
    def verify_document(doc: Dict[str, Any]) -> bool:
        """Verify document has all required fields."""
        return bool(doc and all(field in doc for field in SalesRepository.REQUIRED_FIELDS))

    @staticmethod
    def build_time_series_query(app_id: int, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Build query for time series data."""
        return {
            'aid': app_id,
            'd': {
                '$gte': start_date,
                '$lte': end_date
            }
        }

    @staticmethod
    def get_projection() -> Dict[str, Any]:
        """Get projection for time series query."""
        return {'d': 1, 'ir': 1, '_id': 0}