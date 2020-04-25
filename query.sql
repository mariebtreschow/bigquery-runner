select count(unique_key) as number_of_cases,
extract(dayofweek from date) as day_of_week
from bigquery-public-data.chicago_crime.crime
where arrest is true
group by day_of_week
order by number_of_cases asc;