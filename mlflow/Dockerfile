FROM python:3.9.6-slim

RUN pip install mlflow==1.20.0
RUN pip install psycopg2-binary

EXPOSE 5000
RUN mkdir -p /startup 
WORKDIR /startup
COPY wait-for-it.sh /startup/.

RUN mkdir -p /mlflow

CMD ./wait-for-it.sh postgresql:5432 -- mlflow server \ 
    --backend-store-uri postgresql://admin:secret@postgresql:5432/mlflow \
    --default-artifact-root /mlflow \
    --host 0.0.0.0