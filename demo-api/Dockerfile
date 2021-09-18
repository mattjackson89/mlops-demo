FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

RUN pip install --upgrade pip
WORKDIR /base
ADD ./requirements.txt /base/requirements.txt
RUN pip install -r requirements.txt

COPY ./app /app
WORKDIR /app
