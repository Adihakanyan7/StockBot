# TODO: write a rty except code for entering incorrect ticker_symbol  -  complete
# TODO: Cancel the message pycharm send when an error accord (not so important for the final project) - already try
#          try:
#              with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")
# TODO: Add code to print_info function, so that it will also print the candlestick chart of the stock  -  complete
# TODO: modularize print_info  -  complete

import yfinance as yf
import mplfinance as mpf


def upper_symbol_ticker(ticker_symbol):
    # convert the word to uppercase
    return ticker_symbol.upper()


def create_ticker_object(ticker_symbol):
    # create a Ticker object
    return yf.Ticker(ticker_symbol)


def get_ticker_data(ticker):
    # fetch historical data
    return ticker.history(period="1y")  # for the last year


def extract_recent_data(historical_data):
    # get most recent trading day's data
    recent_data = historical_data.iloc[-1]
    # extract information for the most recent trading day
    return recent_data['Close'], recent_data['Open'], recent_data['Close'], recent_data['High'], recent_data['Low']


def create_text_message(ticker_symbol, current_price, open_price, close_price, high_price, low_price):
    # Create text message with the required information
    text_message = f"Here are the details for {ticker_symbol} on the most recent trading day:\n"
    text_message += f"Current price: {current_price}\n"
    text_message += f"Opening price: {open_price}\n"
    text_message += f"Closing price: {close_price}\n"
    text_message += f"High price: {high_price}\n"
    text_message += f"Low price: {low_price}"
    return text_message


def create_chart(historical_data, ticker_symbol):
    # Create the candlestick chart and print it to the screen
    mpf.plot(historical_data, type='candle', style='charles', title=f'{ticker_symbol} Stock Price')


def handle_exceptions(exception):
    print("scrapper file - exception")
    raise exception


def print_info(ticker_symbol):
    try:
        ticker_symbol_upper = upper_symbol_ticker(ticker_symbol)
        ticker = create_ticker_object(ticker_symbol_upper)
        historical_data = get_ticker_data(ticker)
        current_price, open_price, close_price, high_price, low_price = extract_recent_data(historical_data)
        text_message = create_text_message(ticker_symbol_upper, current_price, open_price, close_price, high_price,low_price)
        print(text_message)
        create_chart(historical_data, ticker_symbol_upper)

    # re-raise the exception to calling code
    except (KeyError, IndexError, ConnectionError, TimeoutError, ValueError, Exception) as e:
        handle_exceptions(e)

