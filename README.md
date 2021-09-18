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
python data-engineering/ingest/upload.py --data_loc raw-data --file_name compounds.json --output_path data-science/data --dlq dlq.log
```

For full details see [the data-engineering README](data-engineering/README.md)

## Modelling 
Both data and modelling are itterative processes. This demo aims to demostrate how this might work in an operational environment. Use the link provided by Docker to access the data-science notebook environment and follow the instructions in `train_v1.pynb`. In the notebook we; 

* Train a simple toy model 
* Evaluate the results (badly) 
* Use MLFlow to track the model performance across runs 
* Save the model 

Once the notebook has ran, please go ahead and the following from your command line; 

```
./update-models.sh v1
```

This will update the models for our API and promote v1 to latest. 

A model tracking system such as the one demonstrated here is vital to allow the required iteration on modelling and data. Additional steps could include;
* Saving the model pre-processing steps either as a pipeline to save with the model or as a package to deploy with the API
* Use the MLFlow Model registry backed by s3 to log models and make deployment even easier 
* Use the `data-science` environment to improve the model further 

## Deployment 
For this example I have built a `demo-api`; a super simple API where we can get some model predictions. This locally deployed API could be deployed on AWS ECS or alternative. Our v1 model should be deployed, we can make some calls. 


