import logging
from constants import *


# Logging setup
logging.basicConfig(level=logging.INFO)


def start(update, context):
    """Send a message when the command /start is issued."""
    welcome_message = "Welcome to the StockBot! Type 'help' to see how to use me."
    context.bot.send_message(chat_id=update.effective_chat.id, text=welcome_message)


def handle_add_alert(context, chat_id, stock_name, direction, price_target):
    """Handle adding an alert."""
    try:
        if not parser.is_valid_stock_name(stock_name):
            stock_service.send_bot_message(context, chat_id, INVALID_STOCK_MSG)
            return
        db_manager.add_alert(chat_id, stock_name, direction, price_target)
        stock_service.send_bot_message(context, chat_id, ALERT_ADD_MSG.format(stock_name, direction, price_target))
    except Exception as e:
        logging.error(f"Error while adding alert for {stock_name}: {e}")
        stock_service.send_bot_message(context, chat_id, ERROR_MSG)


def handle_remove_alert(context, chat_id, stock_name, direction, price_target):
    """Handle removing an alert."""
    try:
        db_manager.remove_alert(chat_id, stock_name, direction, price_target)
        stock_service.send_bot_message(context, chat_id, ALERT_REMOVE_MSG.format(stock_name, direction, price_target))
    except Exception as e:
        logging.error(f"Error while removing alert for {stock_name}: {e}")
        stock_service.send_bot_message(context, chat_id, ERROR_MSG)


def handle_info_request(context, chat_id, stock_name):
    """Handle sending stock info and chart."""
    try:
        text_message, historical_data = stock_service.send_message_and_chart(stock_name)
        context.bot.send_message(chat_id=chat_id, text=text_message)

        if not historical_data.empty:  # Check if the DataFrame 'historical_data' is not empty. Using .empty property as directly evaluating a DataFrame for truthiness is ambiguous in Python.
            chart_file_name = os.path.join(CHART_DIRECTORY, f'{stock_name}-chart.png')
            logging.info(chart_file_name)
            logging.info("here")
            stock_service.create_chart(historical_data, stock_name, chart_file_name)
            logging.info(chart_file_name)
            with open(chart_file_name, 'rb') as chart_file:
                context.bot.send_photo(chat_id=chat_id, photo=chart_file)
                logging.info(chart_file)
    except Exception as e:
        logging.error(f"Error while processing info request for {stock_name}: {e}")
        stock_service.send_bot_message(context, chat_id, ERROR_MSG)


def send_help_message(update, context):
    help_message = """
Welcome to StockBot! 📈 Here are the commands you can use:

🔍 Get Stock Information:
"send me info about AAPL"
(Replace 'AAPL' with your desired stock symbol)

🔔 Add an Alert: 
"add alert for AAPL > 150"
(Set an alert for when 'AAPL' exceeds 150; replace 'AAPL' and '150' accordingly)

❌ Remove an Alert: 
"remove alert for AAPL < 130"
(Remove an alert for 'AAPL' dropping below 130; adjust 'AAPL' and '130' as needed)

❓Need Assistance? 
Simply type "help".
"""

    context.bot.send_message(chat_id=update.effective_chat.id, text=help_message)


def handle_stock_request(update, context):
    """Main handler for incoming stock requests."""
    chat_id = update.effective_chat.id
    print("stock_service -> chat_id: ", chat_id)

    # Helper function for parsing errors
    def handle_parsing_error(error_message):
        logging.error(error_message)
        stock_service.send_bot_message(context, chat_id, PARSE_ERROR_MSG)
        return None

    # Helper function to handle service unavailability
    def handle_service_unavailable():
        message = "The stock information service is temporarily unavailable. Please try again later."
        stock_service.send_bot_message(context, chat_id, message)

    try:
        message_text = update.message.text.strip()
        print("stock_service -> message_text", message_text)
        action, stock_name, direction, price_target = parser.parse_user_message(message_text)

        # Check if any parsed item is None or empty
        if not action:
            return handle_parsing_error(f"Incomplete data after parsing: {message_text}")

    except Exception as e:
        return handle_parsing_error(f"Error in parsing user message: {e}")

    try:
        # Check if user requests help
        if action == "help":
            send_help_message(update, context)
            return

        # Handle 'info' action with enhanced error handling
        elif action == "info":
            is_valid, error_type = parser.is_valid_stock_name(stock_name)
            if not is_valid:
                if error_type == "ServiceUnavailable":
                    handle_service_unavailable()
                else:
                    stock_service.send_bot_message(context, chat_id, ERROR_MSG)
                return
            handle_info_request(context, chat_id, stock_name)
        # Handle 'add_alert' action
        elif action == "add_alert":
            handle_add_alert(context, chat_id, stock_name, direction, price_target)
            stock_service.send_bot_message(context, chat_id, SUCCESS_ADDED_MSG)

        # Handle 'remove_alert' action
        elif action == "remove_alert":
            handle_remove_alert(context, chat_id, stock_name, direction, price_target)
            stock_service.send_bot_message(context, chat_id, SUCCESS_REMOVED_MSG)

    except Exception as e:
        logging.error(f"Error in handle_stock_request: {e}")
        stock_service.send_bot_message(context, chat_id, ERROR_MSG)


