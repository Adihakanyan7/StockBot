import logging
import psycopg2

class DatabaseManager:
    def __init__(self, db_url):
        self.database_url = db_url

    def get_connection(self):
        """
        Get a connection to the database.

        Returns:
            Connection object for the PostgreSQL database.
        """
        return psycopg2.connect(self.database_url)

    def setup(self):
        """
        Ensure the database/table is ready.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_alerts (
                        id SERIAL PRIMARY KEY,
                        chat_id INTEGER,
                        stock_name TEXT NOT NULL,
                        direction TEXT NOT NULL,
                        price_target REAL NOT NULL
                    )
                    ''')
                    connection.commit()
        except psycopg2.DatabaseError as e:
            logging.error("Error setting up database: %s", str(e))

    def add_alert(self, chat_id, stock_name, direction, price_target):
        """
        Add a user alert to the database.

        Args:
            chat_id (int): User's chat ID.
            stock_name (str): Name of the stock.
            direction (str): Direction ("up" or "down") for the alert.
            price_target (float): Price target for the alert.

        Raises:
            psycopg2.DatabaseError: If there's an issue interacting with the database.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                    INSERT INTO user_alerts (chat_id, stock_name, direction, price_target)
                    VALUES (%s, %s, %s, %s)
                    ''', (chat_id, stock_name, direction, price_target))
                    connection.commit()
        except psycopg2.DatabaseError as e:
            logging.error("Error adding user alert to db: %s", str(e))

    def remove_alert(self, chat_id, stock_name, direction, price_target):
        """
        Remove a user alert from the database.

        Args:
            chat_id (int): User's chat ID.
            stock_name (str): Name of the stock.
            direction (str): Direction ("up" or "down") for the alert.
            price_target (float): Price target for the alert.

        Raises:
            psycopg2.DatabaseError: If there's an issue interacting with the database.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                    DELETE FROM user_alerts WHERE chat_id = %s AND stock_name = %s AND direction = %s AND price_target = %s
                    ''', (chat_id, stock_name, direction, price_target))
                    connection.commit()
        except psycopg2.DatabaseError as e:
            logging.error("Error removing user alert from db: %s", str(e))

    def fetch_all_alerts(self):
        """
        Fetch all alerts from the database.

        Returns:
            list: List of all alerts in the database.

        Raises:
            psycopg2.DatabaseError: If there's an issue interacting with the database.
        """
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT chat_id, stock_name, direction, price_target FROM user_alerts')
                    return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            logging.error("Error fetching alerts from db: %s", str(e))
            return []

# Don't forget to handle closing the cursor and connection properly, especially if you extend this class in the future.
