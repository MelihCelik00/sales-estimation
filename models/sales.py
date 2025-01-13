from datetime import datetime
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class SalesRecord:
    app_id: int
    date: datetime
    revenue: float
    country: str

    @classmethod
    def from_document(cls, doc: Dict[str, Any]) -> 'SalesRecord':
        """Create SalesRecord from MongoDB document."""
        return cls(
            app_id=doc['aid'],
            date=doc['d'],
            revenue=doc['ir'],
            country=doc['cc']
        )
    
    def to_document(self) -> Dict[str, Any]:
        """Convert to MongoDB document format."""
        return {
            'aid': self.app_id,
            'd': self.date,
            'ir': self.revenue,
            'cc': self.country
        }

