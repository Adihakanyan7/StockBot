import os
from databaseManager import DatabaseManager
from stockService import StockService
from parser import Parser

# Alert messages
ALERT_ADD_MSG = "Got it! I'll alert you when {} goes {} {}."
ALERT_REMOVE_MSG = "Alert for {} when it goes {} {} has been removed."

# Success messages
SUCCESS_ADDED_MSG = "Alert successfully added!"
SUCCESS_REMOVED_MSG = "Alert successfully removed!"
INFO_CHECK_MSG = "Please hold on a moment; I'm checking the details for you."

# Error messages
INVALID_STOCK_MSG = "Invalid stock name provided. Please check and try again."
ERROR_MSG = "Sorry, something went wrong!"
PARSE_ERROR_MSG = "I couldn't understand your request. Please ensure it's in the correct format."

CHART_DIRECTORY = os.path.join(os.getcwd(), 'charts')

# Fetch environment variables for the database
password_db = os.environ.get('PASSWORD_FOR_DB')
username_db = os.environ.get('USERNAME_FOR_DB')
if not password_db or not username_db:
    raise ValueError("Missing database credentials in environment variables!")

DATABASE_URL = f"postgresql://{username_db}:{password_db}@localhost:5432/stock_alerts_db"

# Ensure the directory for charts exists
os.makedirs(CHART_DIRECTORY, exist_ok=True)

# Get token
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

# Initialize services
db_manager = DatabaseManager(DATABASE_URL)
stock_service = StockService()
parser = Parser()
