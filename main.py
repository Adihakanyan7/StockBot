from dispatcher import setup_dispatcher
import os

bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')

if not bot_token:
    raise ValueError("No Telegram bot token found in environment variables!")

updater, dp = setup_dispatcher(bot_token)

def main():
    print("Starting bot...")
    updater.start_polling()
    updater.idle()
    print("Bot stopped.")


if __name__ == "__main__":
    main()
