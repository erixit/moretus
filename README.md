# Moretus Application

A Streamlit web application with SQLite database integration.

## Project Structure

```
moretus/
├── app.py                 # Main Streamlit application
├── database.py            # SQLite database module
├── team_manager.py        # Team selection rules engine
├── requirements.txt       # Python dependencies
├── .env.example          # Environment configuration template
├── .gitignore            # Git ignore rules
├── TEAM_SELECTION.md     # Team selection rules documentation
├── README.md             # This file
└── sql/
    └── moretus_sqlite.sql # SQLite schema and sample data
```

## Features

- **Streamlit Web UI**: Interactive web interface built with Streamlit
- **SQLite Database**: Local database for data persistence
- **Player Management**: View all registered chess players with ELO ratings
- **Team Selection**: Select 6 players and create valid team configurations
- **Team Rules Engine**: Enforces ±2 board placement rules from strength list ranking
- **Configuration Analysis**: Shows all possible valid team compositions
- **Dashboard**: Analytics and monitoring capabilities
- **Settings**: Application configuration options

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd c:\msi_projects\moretus
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create environment file**:
   ```bash
   copy .env.example .env
   ```
   Then edit `.env` with your configuration.

## Running the Application

1. **Start the Streamlit server**:
   ```bash
   streamlit run app.py
   ```

2. **Access the application**:
   - The application will open in your default browser at `http://localhost:8501`
   - If not, navigate to the URL shown in the terminal

## Usage

### Navigation Menu
- **Home**: Overview and database status
- **Players**: View all chess players sorted by strength list ELO
- **Team Selection**: Select 6 players and create valid team configurations
- **Data Manager**: View, add, and delete records
- **Analytics**: View dashboard and statistics
- **Settings**: Configure application behavior

### Database Operations
The `database.py` module provides methods for:
- Inserting records: `insert_record()`
- Fetching records: `fetch_one()`, `fetch_all()`
- Updating records: `update_record()`
- Deleting records: `delete_record()`
- Executing queries: `execute_query()`

## Team Selection Rules

The application implements chess club team selection rules:

### Team Composition
- Select exactly 6 players from available roster
- Players ranked by Strength List ELO (strongest first)

### Board Placement Rules
- Each player can be placed **maximum ±2 boards** from their strength list rank
- Example: 3rd-ranked player can play on boards 1-5
- The system calculates all valid team configurations and picks one

### Features
- Visual player selection interface
- Automatic rule compliance validation
- Display count of all possible valid configurations
- Show board assignments for selected team
- Rule compliance verification table
- Export team to CSV or JSON

For detailed rules, see [TEAM_SELECTION.md](TEAM_SELECTION.md)

## Example: Using the Team Selection

1. Navigate to "Team Selection" page
2. Select 6 players from the displayed strength list
3. Click "🏆 Create Team" button
4. View:
   - Selected players sorted by board position
   - Number of possible valid configurations
   - Rule compliance for each player
   - Team statistics (average ELO, total ELO, etc.)
5. Export team configuration as CSV or JSON

## Example: Using the Database

```python
from database import Database

# Initialize database
db = Database("moretus.db")

# Insert a record
record_id = db.insert_record("records", {
    "name": "Test Record",
    "value": 100.0,
    "description": "A test record"
})

# Fetch all records
all_records = db.fetch_all("SELECT * FROM records")

# Update a record
db.update_record("records", 
    {"value": 150.0}, 
    {"id": record_id}
)

# Delete a record
db.delete_record("records", {"id": record_id})

# Close connection
db.close()
```

## Configuration

Edit `.env` file to customize:
- `DB_PATH`: Location of SQLite database file
- `STREAMLIT_DEBUG`: Enable debug mode
- `APP_ENV`: Development or production mode
- `LOG_LEVEL`: Logging verbosity

## Deployment

For deploying to a **Raspberry Pi** or other webserver, see [DEPLOYMENT_RASPBERRYPI.md](DEPLOYMENT_RASPBERRYPI.md)

Quick summary:
- Transfer files to Pi via Git or SCP
- Create virtual environment: `python3 -m venv venv`
- Install dependencies: `pip install -r requirements.txt`
- Run as systemd service for persistence
- Optional: Use Nginx as reverse proxy on port 80

## Database Schema

### Records Table
```sql
CREATE TABLE records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    value REAL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

Customize this schema in `database.py` `_initialize_tables()` method as needed.

## Troubleshooting

### Port Already in Use
If port 8501 is already in use, Streamlit will automatically use the next available port.

### Database Lock Error
Ensure only one instance of the application is running. If you encounter lock errors, restart the application.

### Dependencies Not Installing
Make sure your Python version is 3.8 or higher:
```bash
python --version
```

## Development Tips

1. **Hot Reload**: Streamlit automatically reloads when you save changes
2. **Clear Cache**: Use Ctrl+C in the terminal to stop the server
3. **Debug Mode**: Set `STREAMLIT_DEBUG=true` in `.env` for verbose logging

## Next Steps

1. Customize the database schema in `database.py`
2. Add more pages/tabs in `app.py`
3. Implement data validation
4. Add user authentication
5. Create data export functionality
6. Add charts and visualizations

## License

MIT License

## Support

For issues or questions, check the [Streamlit documentation](https://docs.streamlit.io) or [SQLite documentation](https://www.sqlite.org/docs.html).
