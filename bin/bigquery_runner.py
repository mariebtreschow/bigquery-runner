#!/bin/python3
import os
import sys
import csv
import logging
import sqlvalidator
from datetime import datetime
from google.cloud import bigquery
from logging.config import fileConfig


# Defining logging level
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')
logging.basicConfig(level=LOGGING_LEVEL)
fileConfig(os.path.dirname(__file__) + '/../logging.conf')
logger = logging.getLogger(__name__)

# TODO: CONVERT TIME FOR DOCKER
# TODO: fix file submittion on docker and json credentials


def get_query():
    """Try reading the file submitted on the command line"""
    try:
        file = open(sys.argv[1], 'r')
        query = file.read()
        file.close()
        return query
    except IndexError:
        logger.warning("You need to submit a sql file with the query you want to run")
        sys.exit(1)


def validate_query(query):
    """Validate query submitted through the command line in a sql file format"""
    sql_query = sqlvalidator.parse(query)
    if not sql_query.is_valid():
        raise SyntaxError('Your query could not be parsed with the following error {}'.format(sql_query.errors))
    return True


def run(query):
    """Running a SQL query on google environment provided in the command line returns a CSV file with the results"""
    logger.info("Running SQL query {} in BigQuery...".format(query))

    client = bigquery.Client()
    query_job = client.query("""{}""".format(query))
    try:
        results = query_job.result()
    except Exception as error:
        logger.error(error)
        sys.exit(1)

    logger.info("Writing result to a CSV file in the csv_results folder...")
    now = datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    try:
        with open('csv_results/query-runner-result-{}.csv'.format(now),
                  'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for i, row in enumerate(results):
                if i == 0:
                    headers = [header for header in row.keys()]
                    writer.writerow(headers)
                row = [row for row in row.values()]
                writer.writerow(row)
    except PermissionError as error:
        logging.error(error)


def global_exception_handler(exc_type, exc_value, traceback):
    """Global exception handler :param exc_type, exc_value, traceback"""
    logger.error("Logging an uncaught exception",
                 exc_info=(exc_type, exc_value, traceback))


# Exception handler
sys.excepthook = global_exception_handler

if __name__ == "__main__":
    query = get_query()
    if validate_query(query):
        run(query)
    else:
        logger.warning(''.join(['SQL query is not valid']))
