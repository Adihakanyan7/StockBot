import schedule
import time
import logging

from dotenv import load_dotenv
load_dotenv()

from dispatcher import setup_dispatcher
from constants import *

# Initialize logging
logging.basicConfig(level=logging.INFO)


# Ensure essential environment variables are set
if not all([bot_token, password_db, username_db]):
    raise ValueError("Essential environment variables not found!")

updater, dp = setup_dispatcher(bot_token)

# Create an instance of DatabaseManager
DB_URL = f"postgresql://{username_db}:{password_db}@localhost:5432/stock_alerts_db"
db_manager = DatabaseManager(DB_URL)


def stock_alert_check_job():
    """
    This job checks stock alerts at a set interval. If any stock hits the alert
    conditions set by the user, the bot sends them a notification.
    """
    try:
        StockService.check_stock_alerts(db_manager, dp.bot)
    except Exception as e:
        logging.error(f"Error during stock alert check: {e}")
def main():
    logging.info("Starting bot...")

    # Schedule the stock alert check job to run every 10 minutes
    schedule.every(10).minutes.do(stock_alert_check_job)

    # Start polling for updates from Telegram
    updater.start_polling()

    # Keep running the scheduled jobs in the background
    while True:
        schedule.run_pending()
        time.sleep(1)  # Sleep for a second to prevent overloading

    updater.idle()
    logging.info("Bot stopped.")

if __name__ == "__main__":
    main()
