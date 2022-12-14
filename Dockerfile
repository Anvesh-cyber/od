# FROM python:3.8-slim-buster
#
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1
# WORKDIR /app
# EXPOSE 8080
# RUN apt-get update
# RUN apt-get install ffmpeg libsm6 libxext6  -y
#
# COPY requirements.txt requirements.txt
# RUN pip3 install gunicorn
# RUN pip3 install -r requirements.txt
#
# COPY . .
#
# CMD gunicorn --bind 0.0.0.0:8080 app:app
# #CMD gunicorn --bind 0.0.0.0:5000 app:app --daemon


# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5002
COPY . .
CMD ["python3", "-m", "flask", "run","--host=172.17.0.3", "--port=5002"]
