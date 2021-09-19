# mlops-demo
This repo contains an stripped back MLProject and aims to demostrate some key MLOps principles and practices. 

## Aims
* :mechanic: demonstration of some MLOps principles
* :technologist: showcase a variety of experience  
* :astronaut: highlight how a similar system might look outside of this single repo

## Getting Started 
To get the full MLOps experience please continue to run through this README and follow along, at this point you should be in the repos **root directory**. 

### Pre-requisites 
* Docker 
* Access to a unix command line 
* Local python environment running python 3.9.6 or later (this can be achieved using venv, conda or otherwise)
* Installed the local-requirements.txt in your virtual environment  

This can be achived with conda using the following commands
```
conda create --name mlops-demo python=3.9.6 --file local-requirements.txt
conda activate mlops-demo
```

### Start Up
Before we run through the MLFlow demo, let's spin everything we need up, open a new tab and run;

```
docker-compose build && docker-compose up
```

> **Waring** - the first time building the containers may task some time... looking at you Tensorflow! 

> **Note** - This local deployment has multple containers which could be optimsied, if it is struggling ensure Docker has enough CPU and memory access! 

## MLOps
MLOps is responsible for the full lifecycle of a Machine Learning system, the image below is taken from Andrew Ng's Introduction to ML in Production Coursera course and shows the distinct steps of this iterative process.

![Machine Learning Lifecycle](mlops.jfif "MLOps")

### Scoping
For the sake of this story we for some reason have been asked to predict the number of rings in a compound using only the image given in the data set. Expectations are;

* Predictions can be obtained from an API
* The model can be retrained as more data becomes avalable 
* The performance of the model is not important (this is a toy example which might not even work!)

In reality scoping is an extremely important part of the MLOps lifecycle! 

### Data 
It is important to build a data pipeline which delivers a consistent set of data for our needs. A simple tool has been developed to do this via the command line, run with;

```
python data-engineering/ingest/upload.py --data_loc raw-data --file_name compounds.json --output_path data-science/data --dlq data-engineering/ingest/dlq.log
```

I added some "bad data" to show how the dlq might work, it hasn't been processed but you can have a look;

```
less data-engineering/ingest/dlq.log
```

Processed data is now available in `data-science/data` as a single `compound_rings.csv` file and a directory containing the images for training. 

For full details see [the data-engineering README](data-engineering/README.md)

### Modelling 
Both data and modelling are itterative processes. This demo aims to demostrate how this might work in an operational environment. 

One of the containers we started provides a notebooking environment, in the docker-compose tab you should see some logs similar to;

```
data-science_1  |     To access the notebook, open this file in a browser:
data-science_1  |         file:///home/jovyan/.local/share/jupyter/runtime/nbserver-8-open.html
data-science_1  |     Or copy and paste one of these URLs:
data-science_1  |         http://8719d239343f:8888/?token=f23121bbd6745a2754e60c032d5193bbc8bdd7fb4c9d03d8
data-science_1  |      or http://127.0.0.1:8888/?token=f23121bbd6745a2754e60c032d5193bbc8bdd7fb4c9d03d8
```

Use the link to access the data-science notebook environment and follow the instructions in `data-scienc/train.pynb`. In the notebook we; 

* Train a simple toy model 
* Evaluate the results (badly) 
* Use MLFlow to track the model performance across runs 
* Save the model 
* Make a second model to demostrate MLFlow logging and deployment patterns

> See http://localhost:5000/ to view the tracked experiment

Once the notebook has finished running, please go ahead and the following from your command line; 

```
./update-models.sh v1
```

This will update the models for our API and promote v1 to latest. 

A model tracking system such as the one demonstrated here is vital to allow the required iteration on modelling and data. Additional steps could include;
* Saving the model pre-processing steps either as a pipeline to save with the model or as a package to deploy with the API
* Use the MLFlow Model registry backed by s3 to log models and make deployment even easier 
* Use the `data-science` environment to improve the model further 

### Deployment 
For this example I have built a `demo-api`; a super simple API where we can get some model predictions. This locally deployed API could be deployed on AWS ECS or alternative. Our v1 model should be deployed, we can make some calls either in the browser, your favourite tool or with the command line;

```
# Welcome message 
curl -X GET localhost:80

# Check what model versions are avaliable to us 
curl -X GET localhost:80/models/ 

# Check v1 was deployed 
curl -X GET localhost:80/deployed_version/

# Make a prediction 
curl -X POST -F "image=@raw-data/images/2176417.png" localhost:80/predict/
```

Let's promote the v2 model (we can even pretend it was made after v1 had been monitored and we had reacted to some need for perfomance improvements).

```
./update-models.sh v2
```

We can now check the model deployed and make another prediction.

```
# Check v2 was successfully deployed 
curl -X GET localhost:80/deployed_version/

# Make another prediction
curl -X POST -F "image=@raw-data/images/2176417.png" localhost:80/predict/
```

> Some basic documentation for the API can be found at http://localhost:80/docs

:tada: you have reached the end of the demo, we have;
* Pretented to scope a project 
* Looked at some data pipeline principles to support our model training efforts 
* Trained a (terrible) model to predict the number of rings in a compound 
* Tracked model performance using MLFlow
* Deployed different versions of our model using a simple API 

## Next Steps
There are tonnes of things to do! In reality this repo is a reflection of a few different ideas so would likely be split and deployed seperatly. Some things to take forward include; 

* Model monitoring - it is absent from this demo but it is important to track; this could be model metrics e.g. how certain predictions are or even feedback from the user if appropriate. Monitoring allows us to react to changes in data/model performance and alert that retraining may be required 
* API error handling (any)
* Model code is duplicated across training and deployment, packaging or including into the model pipeline is important for consistency
* Utilise MLFlow model registry rather than the how cooked local version here
* CI/CD is important for ease and consistency of deplying production systems, given time I would like to 
    * Add pre-commit hooks to ensure things like linting (e.g. Flake/Black) and security are consistently (e.g. Bandit) dealt with before any commits are made
    * GitHub actions (or alternative) could help deploy the API, ensuring any checks and tests are complete before making a release 
    * Extend testing (currently just a dummy example in the API, to run locally install API requirements and call `pytest test_main.py`)
    * API monitoring - as well as monitoring the models we should monitor the infrastructure and performance
* More consistent versioning and requirements management
* Environment specific config (dev, prod etc)
* Lots of model development!! 


