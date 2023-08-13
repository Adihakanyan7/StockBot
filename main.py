from scrapper import print_info
import warnings
# TODO write a rty except code for entering incorrect ticker_symbol

if __name__ == '__main__':
    run = True
    while run:
        try:
            # get a ticker symbol from the user
            ticker_symbol = input('pleas enter a ticker symbol (to quit press "q"): ')
            if ticker_symbol == 'q':
                print("see you next time :)")
                run = False
                break

            # print the data and the candlestick chart stock
            print_info(ticker_symbol)
        except KeyError as key:
            print("A key error occurred pleas try agine.")
            continue
        except IndexError as index:
            print("An index error occurred pleas try agine.")
            continue
        except ConnectionError as connect:
            print("A connection error occurred pleas try agine.\n")
            continue
        except TimeoutError as time:
            print("The request timed out pleas try agine.\n")
            continue
        except ValueError as value:
            print("An invalid value was provided pleas try agine.\n")
            continue
        except Exception as e:
            print(f"An unexpected error occurred: {e} pleas try agine\n")
            raise e

