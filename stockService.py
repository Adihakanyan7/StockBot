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
        mpf.plot(historical_data, type='candle', style='charles', title=f'{ticker_symbol.upper()} Stock Price',
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

    @staticmethod
    def check_stock_alerts(db_manager, bot_context):
        """Check the alerts set by users against current stock prices."""
        alerts = db_manager.fetch_all_alerts()

        for alert in alerts:
            chat_id, stock_name, direction, price_target = alert

            try:
                stock = yf.Ticker(stock_name)
                current_price = stock.history(period="1d")["Close"].iloc[-1]
            except Exception as e:
                logging.error(f"Error fetching data for {stock_name}: {e}")
                continue

            if (direction == ">" and current_price > price_target) or (
                    direction == "<" and current_price < price_target):
                StockService.send_bot_message(bot_context, chat_id,
                                              f"Alert! {stock_name} has reached {current_price}. Your target was {direction}")
