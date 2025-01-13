# iTunes App Sales Time Series Query

This project implements an optimized time series query system for iTunes App Store sales data. It handles a large-scale MongoDB collection containing daily download and revenue data for millions of apps.

## Problem Description

The system tracks daily downloads and revenue for applications on the iTunes store, storing data for:
- Each day
- Each country
- Each app

The data is stored in a MongoDB collection called `itunes_sales_report_estimates`. With almost 10 billion records, the system is optimized for efficient time-series queries. The dataset covers revenue data for tested appId from January 1, 2014, to December 23, 2019.

## Requirements

### System Requirements
- Python 3.9+
- MongoDB Database Tools
- Virtual Environment support

### Python Dependencies
- pymongo
- python-dotenv
- python-dateutil
- dnspython
- setuptools

### MongoDB
- MongoDB Atlas account (or local MongoDB server)
- MongoDB connection string

## Setup Instructions

1. **Clone the Repository**
```bash
git clone <repository-url>
cd <repository-directory>
```

2. **Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Install MongoDB Tools** (if not already installed)
```bash
# On macOS
brew install mongodb-database-tools

# On Ubuntu
sudo apt-get install mongodb-database-tools
```

5. **Configure MongoDB Connection**
Create a `.env` file in the project root:
```bash
MONGODB_URI=your_mongodb_atlas_connection_string
```

6. **Run Initial Setup**
```bash
python main.py --setup
```
This will:
- Restore the MongoDB dump
- Create necessary indexes

## Usage

### Basic Query
```bash
python main.py
```

### Example Input/Output
```python
# Input parameters
app_id = 7118
start_date = '2017-01-01'
end_date = '2017-01-03'

# Output
Revenue time series for app 7118 from 2017-01-01 to 2017-01-03:
[20170101, 20170102, 20170103]
```

### Function Signature
```python
def get_time_series(app_id, start_date, end_date):
    """
    Get iTunes revenue time series for a specific app between start and end dates.
    
    Args:
        app_id (int): The app ID to query
        start_date (datetime): Start date of the time range
        end_date (datetime): End date of the time range
        
    Returns:
        list: List of daily revenue values
    """
```

## Data Structure

### MongoDB Document Schema
```javascript
{
    'd': Date,      // Date of the record
    'cc': String,   // Country code
    'aid': Integer, // App ID
    'ir': Integer   // iPhone revenue
}
```

### Indexes
- Compound index on `(aid, d)` for efficient app-specific date range queries

## Optimizations

1. **Efficient Querying**
   - Uses compound indexes for fast time-range queries
   - Projects only necessary fields
   - Sorts at database level

2. **Data Integrity**
   - Transaction support for data restoration
   - Verification of data structure
   - Automatic index creation

3. **Connection Management**
   - Connection pooling
   - Timeout handling
   - Error recovery

## Error Handling

The script handles various error scenarios:
- Missing virtual environment
- Missing MongoDB connection
- Failed data restoration
- Invalid data structure
- Network issues
