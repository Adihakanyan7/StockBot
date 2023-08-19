# Stock Info & Alert Telegram Bot

Welcome to the Stock Info & Alert Telegram Bot! Your go-to source for fetching latest stock information and setting personalized stock alerts directly within Telegram.

## Features

- **Real-time Stock Information**: Get up-to-date stock details and historical charts with a simple command.
- **Instant Notifications**: Set up alerts and receive notifications immediately when a stock hits your target price.
- **Intuitive Commands**: A user-friendly interface ensures easy access to the bot's features.
- **Manage Alerts**: Set, view, and remove stock alerts as per your preferences.

## Architecture

This bot comprises three primary components:

1. **parser.py** - Extracts and interprets user messages.
2. **stockService.py** - Manages tasks related to obtaining and presenting stock data.
3. **databaseManager.py** - Looks after all database operations, ensuring efficient storage and management of your alerts.

## How to Use the Bot

1. **Connect with the Bot**: 
   
   Simply search for [@AMarketStockBot](https://t.me/AMarketStockBot) on Telegram and initiate a chat.

2. **Use Commands**:
   
   - **/start**: Begin your journey with the bot.
   - **Help**: View a list of available commands.
   - **Send me info about [STOCK_NAME]**: Obtain comprehensive data about a designated stock.
   - **Add alert for [STOCK_NAME] [DIRECTION] [PRICE]**: Set a price alert for timely updates.
   - **Remove alert for [STOCK_NAME] [DIRECTION] [PRICE]**: Erase a pre-set price alert.

Engage with the bot with ease! No downloads. No installations. Just initiate and let the bot cater to your needs.

## For Developers and Contributors

### Setup & Deployment

#### Prerequisites:

- Python3
- PostgreSQL database
- A remote hosting platform (like DigitalOcean, AWS EC2, or Heroku)

#### Deployment Steps:

1. **Install Dependencies**:
   
   ```bash
   pip install yfinance mplfinance psycopg2
