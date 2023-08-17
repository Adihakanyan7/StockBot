import os
import logging

from databaseManager import DatabaseManager
from stockService import StockService

# Logging setup
logging.basicConfig(level=logging.INFO)

# Constants
ERROR_MESSAGE = "An error occurred. Please try again later."
INVALID_STOCK_MSG = "Invalid stock name provided. Please check and try again."
ALERT_ADD_MSG = "Got it! I'll alert you when {} goes {} {}."
ALERT_REMOVE_MSG = "Alert for {} when it goes {} {} has been removed."
CHART_DIRECTORY = os.path.join(os.getcwd(), 'charts')

# Environment variables for DB
password_db = os.environ.get('PASSWORD_FOR_DB')
username_db = os.environ.get('USERNAME_FOR_DB')

if not password_db or not username_db:
    raise ValueError("No password for DB found in environment variables!")

DATABASE_URL = f"postgresql://{username_db}:{password_db}@localhost:5432/stock_alerts_db"

# Initializing services
db_manager = DatabaseManager(DATABASE_URL)
stock_service = StockService()

# Ensure the directory for charts exists, if not, it creates it.
os.makedirs(CHART_DIRECTORY, exist_ok=True)


def handle_add_alert(context, chat_id, stock_name, direction, price_target):
    """Handle adding an alert."""
    if not stock_service.is_valid_stock_name(stock_name):
        stock_service.send_bot_message(context, chat_id, INVALID_STOCK_MSG)
        return
    db_manager.add_alert(chat_id, stock_name, direction, price_target)
    stock_service.send_bot_message(context, chat_id, ALERT_ADD_MSG.format(stock_name, direction, price_target))


def handle_remove_alert(context, chat_id, stock_name, direction, price_target):
    """Handle removing an alert."""
    db_manager.remove_alert(chat_id, stock_name, direction, price_target)
    stock_service.send_bot_message(context, chat_id, ALERT_REMOVE_MSG.format(stock_name, direction, price_target))


def handle_info_request(context, chat_id, stock_name):
    """Handle sending stock info and chart."""
    text_message, historical_data = stock_service.send_message_and_chart(stock_name)
    context.bot.send_message(chat_id=chat_id, text=text_message)

    if historical_data is not None:
        chart_file_name = os.path.join(CHART_DIRECTORY, f'{stock_name}-chart.png')
        stock_service.create_chart(historical_data, stock_name, chart_file_name)
        with open(chart_file_name, 'rb') as chart_file:
            context.bot.send_photo(chat_id=chat_id, photo=chart_file)


def handle_stock_request(update, context):
    """Main handler for incoming stock requests."""
    try:
        message_text = update.message.text.strip()
        action, stock_name, direction, price_target = stock_service.parse_user_message(message_text)

        if action == "add_alert":
            handle_add_alert(context, update.effective_chat.id, stock_name, direction, price_target)
        elif action == "remove_alert":
            handle_remove_alert(context, update.effective_chat.id, stock_name, direction, price_target)
        elif action == "info":
            handle_info_request(context, update.effective_chat.id, stock_name)
    except Exception as e:
        logging.error("Error in handle_stock_request: %s", str(e))
        stock_service.send_bot_message(context, update.effective_chat.id, ERROR_MESSAGE)
