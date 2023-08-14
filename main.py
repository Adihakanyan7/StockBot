from scrapper import print_info


# TODO: write a try  except code for entering incorrect ticker_symbol  -  complete
# TODO: modularize main function  -  complete

def get_ticker_symbol():
    return input('Please enter a ticker symbol (to quit press "q"): ')


def handle_exceptions(exception):
    error_messages = {
        KeyError: "A key error occurred. Please try again.",
        IndexError: "An index error occurred. Please try again.",
        ConnectionError: "A connection error occurred. Please try again.",
        TimeoutError: "The request timed out. Please try again.",
        ValueError: "An invalid value was provided. Please try again.",
        Exception: f"An unexpected error occurred: {e}. Please try again."
    }
    print(error_messages.get(type(exception), f"An unexpected error occurred: {exception}. Please try again."))


if __name__ == '__main__':
    run = True
    while run:
        try:
            ticker_symbol = get_ticker_symbol()
            if ticker_symbol == 'q':
                print("See you next time :)")
                run = False
                break
            print_info(ticker_symbol)
        except (KeyError, IndexError, ConnectionError, TimeoutError, ValueError, Exception) as e:
            handle_exceptions(e)
