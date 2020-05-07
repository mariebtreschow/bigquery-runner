select total_number_of_cases, arrest_count, day_of_week, arrest_count/total_number_of_cases as ratio from (select count(arrest) as total_number_of_cases,
sum(case when arrest then 1 else 0 end) as arrest_count,
extract(dayofweek from date) as day_of_week
from bigquery-public-data.chicago_crime.crime
group by day_of_week) order by ratio asc