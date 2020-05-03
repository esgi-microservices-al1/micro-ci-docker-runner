FROM python:3.7.7-alpine

WORKDIR /opt/project

COPY . .
RUN pip install pipenv
RUN pipenv install --skip-lock --dev --system