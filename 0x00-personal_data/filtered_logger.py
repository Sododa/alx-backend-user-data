#!/usr/bin/env python3
"""data project
"""


import logging
import os
import mysql.connector
import re
from typing import List


patterns = {
    'extract': lambda x, y: r'(?P<field>{})=[^{}]*'.format('|'.join(x), y),
    'replace': lambda x: r'\g<field>={}'.format(x),
}
# Tuple of PII fields
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class

    Update the class to accept a list of strings
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Initializes the clas
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log rec
        """
        # Call the parent class's format method to get the formatted log line
        msg = super(RedactingFormatter, self).format(record)
        # Use the filter_datum function to perform substitution of self.fields
        text = filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
        return text


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str,
) -> str:
    """Returns the log message with certain fields obfuscated.
    """
    extract, replace = (patterns["extract"], patterns["replace"])
    return re.sub(extract(fields, separator), replace(redaction), message)


def get_logger() -> logging.Logger:
    """Returns a logging.Logger object named "user_data".

    The logger should be named "user_data" and only log up to logging.
    """
    # Create a logger with the specified name
    logger = logging.getLogger("user_data")
    # Set the logging level to only log messages up to logging.INFO
    logger.setLevel(logging.INFO)
    # Create a StreamHandler to output log messages to the console
    stream_handler = logging.StreamHandler()
    # Disable popagation of log messages to other loggers
    logger.propagate = False
    # Create an instance of the RedactingFormatter class with the PII_FIELDS,
    # as fields and set the formatter of the handler
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    # Add the handler to the logger
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connector to the database
    (mysql.connector.conne
    """
    # Get the environment variables for the database credentials
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    #  OR db_name = os.environ.get('PERSONAL_DATA_DB_USERNAME', 'root')
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    db_user = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_pwd = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    # Connect to the database using the obtained credentials
    connection = mysql.connector.connect(
        host=db_host,
        port=3306,
        user=db_user,
        password=db_pwd,
        database=db_name,
    )
    return connection


def main() -> None:
    """Obtains a database connection using get_db and
    """
    # Obtain a logger and set the logging level
    logger = get_logger()
    logger.setLevel(logging.INFO)

    # Obtain a database connection
    db = get_db()
    cursor = db.cursor()

    # Retrieve all rows in the users table
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Display each row under a filtered format
    for row in rows:
        message = "; ".join([f"{field}={row[field]}" for field in row.keys()])
        logger.info(filter_datum(PII_FIELDS, RedactingFormatter.REDACTION,
                                 message, RedactingFormatter.SEPARATOR))


if __name__ == "__main__":
    main()
