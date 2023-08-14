from telegram.ext import Updater, MessageHandler, Filters
from scrapper import *


def send_chart(update, context):
    # Extract the ticker symbol from the message text
    ticker_symbol = update.message.text
    text_message, historical_data = send_info(ticker_symbol)
    if historical_data is not None:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)

        chart_file_name = 'chart.png'
        create_chart(historical_data, ticker_symbol, chart_file_name)
        context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(chart_file_name, 'rb'))
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text=text_message)

# Bot token
bot_token = '6517573892:AAG49U7MO_EMG_YP2wZE9YM2-cg3Wiwa-zE'

# Create Updater and Dispatcher
updater = Updater(bot_token)
dp = updater.dispatcher

# Listen for any text message (not just commands) and call send_chart when one is received

dp.add_handler(MessageHandler(Filters.text & ~Filters.command, send_chart))

# Start the bot
updater.start_polling()
updater.idle()
