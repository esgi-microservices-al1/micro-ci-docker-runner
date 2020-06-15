FROM python:3.7.7-alpine

WORKDIR /opt/project

COPY . .
RUN pip install pipenv
RUN pip install pika
RUN pip install docker
RUN pipenv install --skip-lock --dev --system

CMD python -u /opt/project/main/start.py