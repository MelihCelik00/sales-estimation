import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from core.database import MongoDBManager
from services.setup_service import SetupService
from services.query_service import QueryService
from core.logger import setup_logger

logger = setup_logger(__name__)

def main():
    load_dotenv()
    
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        logger.error("MONGODB_URI not found in environment variables")
        sys.exit(1)
    
    with MongoDBManager(mongodb_uri) as db_manager:
        if len(sys.argv) > 1 and sys.argv[1] == '--setup':
            logger.info("Running one-time MongoDB setup...")
            setup_service = SetupService(db_manager)
            if not setup_service.verify_and_restore_data():
                sys.exit(1)
            logger.info("MongoDB setup completed successfully!")
        else:
            try:
                app_id = 7118
                start_date = datetime.strptime('2017-01-01', '%Y-%m-%d')
                end_date = datetime.strptime('2017-01-03', '%Y-%m-%d')
                
                query_service = QueryService(db_manager)
                result = query_service.get_time_series(app_id, start_date, end_date)
                
                logger.info(f"Revenue time series for app {app_id} from {start_date.date()} to {end_date.date()}:")
                print(result)
            except Exception as e:
                logger.error(f"Error running the script: {e}")
                sys.exit(1)

if __name__ == '__main__':
    main() 