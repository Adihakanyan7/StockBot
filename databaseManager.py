import logging
import psycopg2
from typing import List, Tuple, Optional

class DatabaseManager:
    def __init__(self, db_url: str):
        self.database_url = db_url

    def get_connection(self) -> psycopg2.extensions.connection:
        """Get a connection to the database."""
        return psycopg2.connect(self.database_url)

    def setup(self) -> None:
        """Ensure the database/table is ready."""
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
            logging.info("Database setup successfully or already initialized.")
        except psycopg2.DatabaseError as e:
            logging.error("Error setting up database: %s", str(e))

    def add_alert(self, chat_id: int, stock_name: str, direction: str, price_target: float) -> None:
        """Add a user alert to the database."""
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                    INSERT INTO user_alerts (chat_id, stock_name, direction, price_target)
                    VALUES (%s, %s, %s, %s)
                    ''', (chat_id, stock_name, direction, price_target))
                    connection.commit()
            logging.info(f"Added alert for {stock_name} with target {price_target} on direction {direction}.")
        except psycopg2.DatabaseError as e:
            logging.error("Error adding user alert to db: %s", str(e))

    def remove_alert(self, chat_id: int, stock_name: str, direction: str, price_target: float) -> None:
        """Remove a user alert from the database."""
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('''
                    DELETE FROM user_alerts WHERE chat_id = %s AND stock_name = %s AND direction = %s AND price_target = %s
                    ''', (chat_id, stock_name, direction, price_target))
                    connection.commit()
            logging.info(f"Removed alert for {stock_name} with target {price_target} on direction {direction}.")
        except psycopg2.DatabaseError as e:
            logging.error("Error removing user alert from db: %s", str(e))

    def fetch_all_alerts(self) -> List[Tuple[int, str, str, float]]:
        """Fetch all alerts from the database."""
        try:
            with self.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute('SELECT chat_id, stock_name, direction, price_target FROM user_alerts')
                    return cursor.fetchall()
        except psycopg2.DatabaseError as e:
            logging.error("Error fetching alerts from db: %s", str(e))
            return []
