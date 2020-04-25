# BigQuery runner 
Run a query from the command line to BigQuery that writes the output to a CSV file.

How to use the query runner:

1. Git clone the repository
2. Activate python virtual environment
       
       source venv/bin/activate 
       
3. pip install requirements with the command

        pip3 install -r requirements.txt
        
    
Run command to write output to CSV file

    python3 bin/bigquery_runner.py path/to/your/file.sql

You can find the following results written to a CSV in the csv_results folder.

Example command:

     python3 bin/bigquery_runner.py chicago_crime_preview_10.sql


## Build a Docker image and run from the command line

Build the Docker image

     docker build --rm -t bigquery-runner ./

Run the docker image

    docker run -v $PWD:/csv-result bigquery-runner lowest_crime_rate_per_day.sql 
