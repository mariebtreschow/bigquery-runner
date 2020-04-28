# BigQuery runner 
Run a query from the command line to BigQuery that writes the output to a CSV file.
You need to have Python 3 along with pip, the python package installer installed or you
can build the docker image and run it (see instructions below). 

How to use the query runner:

1. Git clone the repository and install python virtual environment
    
        pip3 install virtualenv
        
2. Create the virtual environment
        
        virtualenv -p python3 venv
        
3. Activate python virtual environment
       
       source venv/bin/activate 
       
4. pip install requirements with the command

       pip3 install -r requirements.txt
        
5. Set the environment variable pointing to your json service account file

       export GOOGLE_APPLICATION_CREDENTIALS=service-account-file.json

    
Run command to write output to CSV file

    python3 bin/bigquery_runner.py path/to/your/file.sql

You can find the following results written to a CSV in the csv_results folder

Example command:

     python3 bin/bigquery_runner.py sql_queries/chicago_crime_preview_10.sql


## Build a Docker image and run from the command line

Add the sql files with the queries you want to run to the sql_queries folder in the project.

Build the Docker image

     docker build --rm -t bigquery-runner .

Run the docker image with the provided path to where you wish to store your CSV file

    docker run -v /path/to/your/folder:/app/csv_results bigquery-runner sql_queries/chicago_crime_preview_10.sql 

Example:
    
     docker run -v ${PWD}/csv_results:/app/csv_results bigquery-runner sql_queries/chicago_crime_preview_10.sql 
     
If you want to use your own google application credentials you can do so by adding the GOOGLE_APPLICATION_CREDENTIALS
environment variable on the run command with the value set to the path of your json file


     docker run -e GOOGLE_APPLICATION_CREDENTIALS="service-account-file.json" -v ${PWD}/csv_results:/app/csv_results bigquery-runner sql_queries/lowest_crime_rate_per_day.sql 