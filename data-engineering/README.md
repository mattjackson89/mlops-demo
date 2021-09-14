# Data Engineering
Data Pipelines form an important part of any operational machine learning system, they provide;

* Consistent access to data for Data Scientists and operational systems 
* Visibility of data processing, errors and bottlenecks
* Scheduling of dependant processes   

This area provides a very minimal example of some data ingest which can be ran locally. 

## Deployment Patterns 
There are many options to deploy data pipelines, in reality a mixture of tools are often used. For a simple script like this a suggested pattern would be to use AWS lambda triggered by a drop of new data in an s3 bucket, a step function could be used to clean up the files after processing. Cloudwatch could be used to monitor metrics and alert if neccessary. A more complex pipeline with dependencies could make use of a scheduling tool such as AirFlow. 

## Data Storage
For the scope of this project the assay results data was not used, therefore a simple csv file was saved to support the data. As the json data is small and further information is easily obtained, in future it might be useful to store this data in something like DynamoDb to enable querying the more complex structure. 