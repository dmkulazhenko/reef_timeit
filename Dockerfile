FROM python:3.8-alpine


RUN mkdir /app
WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn mysql-connector-python
