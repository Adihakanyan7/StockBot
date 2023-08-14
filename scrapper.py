# TODO: write a rty except code for entering incorrect ticker_symbol  -  complete
# TODO: Cancel the message pycharm send when an error accord (not so important for the final project) - already try
#          try:
#              with warnings.catch_warnings():
#                 warnings.simplefilter("ignore")


import yfinance as yf
import mplfinance as mpf
import warnings


def print_info(ticker_symbol):
    try:
        # create a Ticker object
        ticker = yf.Ticker(ticker_symbol)

        # fetch historical data
        historical_data = ticker.history(period="1y")  # for the last year

        # get most recent trading day's data
        recent_data = historical_data.iloc[-1]

        # extract information for the most recent trading day
        current_price = recent_data['Close']
        open_price = recent_data['Open']
        close_price = recent_data['Close']
        high_price = recent_data['High']
        low_price = recent_data['Low']

        # Create text message with the required information
        text_message = f"Here are the details for {ticker_symbol} on the most recent trading day:\n"
        text_message += f"Current price: {current_price}\n"
        text_message += f"Opening price: {open_price}\n"
        text_message += f"Closing price: {close_price}\n"
        text_message += f"High price: {high_price}\n"
        text_message += f"Low price: {low_price}"

        print(text_message)
    # re-raise the exception to calling code\
    except KeyError as key:
        print("Scrapper file: A key error occurred.")
        raise key
    except IndexError as index:
        print("Scrapper file: An index error occurred.")
        raise index
    except ConnectionError as connect:
        print("Scrapper file: A connection error occurred.\n")
        raise connect
    except TimeoutError as time:
        print("Scrapper file: The request timed out.\n")
        raise time
    except ValueError as value:
        print("Scrapper file: An invalid value was provided.\n")
        raise value
    except Exception as e:
        print(f"Scrapper file: An unexpected error occurred: {e}\n")
        raise e
