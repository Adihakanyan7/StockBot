import logging
from telegram.ext import Updater,CommandHandler, MessageHandler, Filters
from stock_service import handle_stock_request, start

# Initialize logging
logging.basicConfig(level=logging.INFO)


def setup_dispatcher(token):
    """
    Setup and return a dispatcher for handling Telegram updates.

    Args:
        token (str): The bot token from Telegram.

    Returns:
        tuple: A tuple containing the updater and dispatcher.
    """
    try:
        updater = Updater(token=token, use_context=True)
        dp = updater.dispatcher

        # Add a message handler for non-command text messages to handle stock requests.
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_stock_request))
        dp.add_handler(CommandHandler("start", start))
        return updater, dp
    except Exception as e:
        logging.error(f"Error setting up dispatcher: {e}")
        return None, None


