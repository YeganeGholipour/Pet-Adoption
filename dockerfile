FROM python:3.9-slim-buster
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

