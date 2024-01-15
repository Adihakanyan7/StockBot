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

# Fetch environment variables for the database and bot token
password_db = os.environ.get('PASSWORD_FOR_DB')
username_db = os.environ.get('USERNAME_FOR_DB')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

# Form the database URL
DATABASE_URL = f"postgresql://{username_db}:{password_db}@{db_host}:{db_port}/{db_name}"

# Ensure the directory for charts exists
os.makedirs(CHART_DIRECTORY, exist_ok=True)

# Initialize services
db_manager = DatabaseManager(DATABASE_URL)
stock_service = StockService()
parser = Parser()
