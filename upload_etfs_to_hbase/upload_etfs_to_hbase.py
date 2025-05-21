import os
import csv
import time
import logging
import happybase

# Constants
ETF_FOLDER = 'ETFs'
TABLE_NAME = 'etfs'
COLUMN_FAMILY = 'data'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def connect_to_hbase(retries=10, delay=5):
    """
    Establishes a connection to HBase with retry logic.

    Args:
        retries (int): Number of retry attempts.
        delay (int): Delay between retries in seconds.

    Returns:
        happybase.Connection: A connection object to HBase.

    Raises:
        ConnectionError: If connection fails after all retries.
    """
    for attempt in range(retries):
        try:
            return happybase.Connection(host='hbase-thrift', port=9090)
        except Exception as e:
            logger.warning(f"Attempt {attempt + 1}: HBase not ready. Retrying in {delay}s...")
            time.sleep(delay)
    raise ConnectionError("Could not connect to HBase after multiple attempts.")

def create_table_if_not_exists(connection):
    """
    Creates the HBase table if it does not already exist.

    Args:
        connection (happybase.Connection): An open HBase connection.
    """
    if TABLE_NAME.encode() not in connection.tables():
        connection.create_table(TABLE_NAME, {COLUMN_FAMILY: dict()})
        logger.info(f"Table '{TABLE_NAME}' created.")
    else:
        logger.info(f"Table '{TABLE_NAME}' already exists.")

def write_csv_to_hbase(connection):
    """
    Reads CSV files from the ETF_FOLDER and inserts their contents into HBase.

    Args:
        connection (happybase.Connection): An open HBase connection.
    """
    table = connection.table(TABLE_NAME)

    for filename in os.listdir(ETF_FOLDER):
        filepath = os.path.join(ETF_FOLDER, filename)
        if os.path.isfile(filepath) and filename.endswith('.txt'):
            etf_name = filename.replace('.txt', '')
            row_count = 0

            with open(filepath, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    date = row['Date']
                    row_key = f"{etf_name}_{date}"
                    table.put(row_key, {
                        f'{COLUMN_FAMILY}:open': row['Open'],
                        f'{COLUMN_FAMILY}:high': row['High'],
                        f'{COLUMN_FAMILY}:low': row['Low'],
                        f'{COLUMN_FAMILY}:close': row['Close'],
                        f'{COLUMN_FAMILY}:volume': row['Volume'],
                        f'{COLUMN_FAMILY}:openint': row['OpenInt'],
                    })
                    row_count += 1

            logger.info(f"Inserted {row_count} rows from '{filename}'.")

def main():
    """
    Main function to connect to HBase, create the table, and upload ETF data.
    """
    connection = connect_to_hbase()
    create_table_if_not_exists(connection)
    write_csv_to_hbase(connection)
    connection.close()

if __name__ == "__main__":
    main()
