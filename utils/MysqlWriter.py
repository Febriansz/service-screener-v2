import mysql.connector
from mysql.connector import Error

def connect_to_mysql(db_config):
    """
    Establish a connection to the MySQL database using the provided configuration.
    """
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def create_results_table(connection):
    """
    Create the screener_results table if it doesn't already exist.
    """
    create_table_query = """
    CREATE TABLE IF NOT EXISTS screener_results (
        service VARCHAR(100),
        region VARCHAR(50),
        check_id VARCHAR(100),
        check_name TEXT,
        status VARCHAR(20),
        severity VARCHAR(20),
        message TEXT,
        timestamp DATETIME
    )
    """
    cursor = connection.cursor()
    cursor.execute(create_table_query)
    connection.commit()
    cursor.close()

def insert_results(connection, results):
    """
    Insert a list of results into the screener_results table.
    Each result should be a dictionary with keys:
    service, region, check_id, check_name, status, severity, message, timestamp
    """
    insert_query = """
    INSERT INTO screener_results (service, region, check_id, check_name, status, severity, message, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor = connection.cursor()
    for result in results:
        cursor.execute(insert_query, (
            result.get('service'),
            result.get('region'),
            result.get('check_id'),
            result.get('check_name'),
            result.get('status'),
            result.get('severity'),
            result.get('message'),
            result.get('timestamp')
        ))
    connection.commit()
    cursor.close()
