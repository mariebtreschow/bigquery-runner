#!/bin/python3
import os
import sys
import csv
import logging
import sqlvalidator
from datetime import datetime
from google.cloud import bigquery
from logging.config import fileConfig


# Should take json credentials on input
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.dirname(__file__) + "/../key-file.json"

# Configuring the logging level of the docker application
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'DEBUG')
logging.basicConfig(level=LOGGING_LEVEL)
fileConfig(os.path.dirname(__file__) + '/../logging.conf')
logger = logging.getLogger(__name__)

# reading the sql file taken as a command line argument
file = open(sys.argv[1], 'r')
QUERY = file.read()
file.close()


def run():
    """Running a SQL query on google environment provided in the command line returns a CSV file with the results"""
    print("Running SQL query {} in BigQuery...".format(QUERY))

    # Connect to google big query and run SQL query TODO: take json on inout file param
    client = bigquery.Client()
    query_job = client.query("""{}""".format(QUERY))
    results = query_job.result()

    print("Writing result to a CSV file in the csv folder...")
    with open('csv_result/query-runner-result-{}.csv'.format(datetime.today().strftime('%Y-%m-%d-%H:%M:%S')),
              'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i, row in enumerate(results):
            if i == 0:
                headers = [header for header in row.keys()]
                writer.writerow(headers)
            row = [row for row in row.values()]
            writer.writerow(row)


def global_exception_handler(exc_type, exc_value, traceback):
    """Global exception handler :param exc_type, exc_value, traceback"""
    logger.error("Logging an uncaught exception",
                 exc_info=(exc_type, exc_value, traceback))


sys.excepthook = global_exception_handler

if __name__ == "__main__":
    sql_query = sqlvalidator.parse(QUERY)
    if sql_query.is_valid():
        run()
    else:
        logger.warning(
            ''.join([
                sql_query.errors
            ])
        )