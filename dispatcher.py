from telegram.ext import Updater, MessageHandler, Filters
from stock_service import handle_stock_request


def setup_dispatcher(token):
    """Setup and return a dispatcher for handling Telegram updates."""
    try:
        updater = Updater(token=token, use_context=True)
        dp = updater.dispatcher

        # Add a message handler for non-command text messages to handle stock requests.
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_stock_request))

        return updater, dp
    except Exception as e:
        print(f"Error setting up dispatcher: {e}")
        return None, None
