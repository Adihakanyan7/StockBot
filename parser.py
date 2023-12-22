import yfinance as yf
import re
import logging
from functools import lru_cache

class Parser:

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
        """Extract the pattern of the message and act accordingly."""

        help_pattern = r"(help)"
        match_help = re.match(help_pattern, message, re.IGNORECASE)

        info_pattern = r"(send me info about|give me details about|tell me about)\s*([\w.]+)"
        match_info = re.match(info_pattern, message, re.IGNORECASE)

        add_pattern = r"(add alert|add alert for)\s+([\w.]+)\s*([<>])\s*([\d.]+)"
        match_add = re.match(add_pattern, message, re.IGNORECASE)

        remove_pattern = r"(remove alert|remove alert for)\s+([\w.]+)\s*([<>])\s*([\d.]+)"
        match_remove = re.match(remove_pattern, message, re.IGNORECASE)

        if match_help:
            return "help", None, None, None
        if match_info:
            stock_name = match_info.groups()[1]
            logging.info(stock_name)
            if Parser.is_valid_stock_name(stock_name):
                return "info", stock_name, None, None
        if match_remove:
            return "remove_alert", match_remove.groups()[1], match_remove.groups()[2], float(match_remove.groups()[3])
        elif match_add:
            return "add_alert", match_add.groups()[1], match_add.groups()[2], float(match_add.groups()[3])
        else:
            return None, None, None, None
