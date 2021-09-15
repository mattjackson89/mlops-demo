# mlops-exsci-demo
This repo contains an stripped back MLProject and aims to demostrate some key MLOps principles and practices. 

## Aims
* :mechanic: demonstration of some MLOps principles
* :technologist: showcase a variety of experience  
* :astronaut: highlight how a similar system might look outside of this single repo

## Getting Started 
To get the full MLOps experience please continue to run through this README and follow along, at this point you should be in the repos root directory. 

## MLOps
MLOps is responsible for the full lifecycle of a Machine Learning system, the image below is taken from Andrew Ng's Introduction to ML in Production Coursera course and shows the distinct steps of this iterative process.

![Machine Learning Lifecycle](mlops.jfif "MLOps")

## Scoping
For the sake of this story we for some reason have been asked to predict the number of rings in a compound using only the image given in the data set. Expectations are;

* Predictions can be obtained from an API
* The model can be retrained as more data becomes avalable 
* The performance of the model is not important (this is a toy example which might not even work!)

In reality scoping is an extremely important part of the MLOps lifecycle! 

## Data 
It is important to build a data pipeline which delivers a consistent set of data for our needs. A simple tool has been developed to do this via the command line, run with;

```
python data-engineering/ingest/upload.py --data_loc raw-data --file_name compounds.json --output_path data-science/data/compound_rings.csv --dlq dlq.log
```

For full details see [the data-engineering README](data-engineering/README.md)
