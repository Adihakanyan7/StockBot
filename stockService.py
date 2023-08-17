import os
import yfinance as yf
import mplfinance as mpf
import re
import logging
from functools import lru_cache

class StockService:

    @staticmethod
    def send_bot_message(context, chat_id, message):
        """Central function to send messages to the user."""
        context.bot.send_message(chat_id=chat_id, text=message)

    @staticmethod
    def create_ticker_object(ticker_symbol):
        """Create and return a ticker object for a given stock symbol."""
        return yf.Ticker(ticker_symbol.upper())

    @staticmethod
    @lru_cache(maxsize=10000)
    def is_valid_stock_name(stock_name):
        """Check if stock name is valid by checking for 'shortName' in its info."""
        try:
            return 'shortName' in yf.Ticker(stock_name).info
        except Exception:
            return False

    @staticmethod
    def parse_user_message(message):
        """Extract stock name, direction ("<" or ">"), and price target from message."""
        # The pattern is  - <stock name>, < "<" or ">" > , <target price>
        print(message)
        info_pattern = r"send me info about\s+([\w.]+)"
        match_info = re.match(info_pattern, message)

        add_pattern = r"add alert\s+([\w.]+)\s*,\s*([<>])\s*,\s*([\d.]+)"
        add_match = re.match(add_pattern, message)

        remove_pattern = r"remove alert\s+([\w.]+)\s+([<>])\s+([\d.]+)"
        match_remove = re.match(remove_pattern, message)
        print(match_info)
        print(add_match)
        print(match_remove)

        if match_info:
            stock_name = match_info.groups()[0]
            if StockService.is_valid_stock_name(stock_name):
                return "info", stock_name, None, None
        if match_remove:
            return "remove_alert", match_remove.groups()[0], match_remove.groups()[1], float(match_remove.groups()[2])
        elif add_match:
            return "add_alert", add_match.groups()[0], add_match.groups()[1], float(add_match.groups()[2])
        else:
            return None, None, None, None

    @staticmethod
    def get_ticker_data(ticker):
        """Fetch historical data for the past year."""
        return ticker.history(period="1y")

    @staticmethod
    def extract_recent_data(historical_data):
        """Get details of the most recent trading day."""
        recent_data = historical_data.iloc[-1]
        return recent_data['Close'], recent_data['Open'], recent_data['Close'], recent_data['High'], recent_data['Low']

    @staticmethod
    def create_text_message(ticker_symbol, current_price, open_price, close_price, high_price, low_price):
        """Format a text message detailing stock info for the most recent trading day."""
        return f"""Here are the details for {ticker_symbol} on the most recent trading day:
    Current price: {current_price}
    Opening price: {open_price}
    Closing price: {close_price}
    High price: {high_price}
    Low price: {low_price}"""

    @staticmethod
    def create_chart(historical_data, ticker_symbol, chart_file_name):
        """Generate a candlestick chart for the given historical data."""
        mpf.plot(historical_data, type='candle', style='charles', title=f'{ticker_symbol} Stock Price',
                 savefig=chart_file_name)

    @staticmethod
    def send_message_and_chart(ticker_symbol):
        """Prepare a message and chart for the provided stock symbol."""
        try:
            ticker = StockService.create_ticker_object(ticker_symbol)
            historical_data = StockService.get_ticker_data(ticker)
            details = StockService.extract_recent_data(historical_data)
            return StockService.create_text_message(ticker_symbol, *details), historical_data
        except Exception as e:
            logging.error("Error in send_message_and_chart: %s", str(e))
            return "I think you entered a wrong name. Please try again.", None
