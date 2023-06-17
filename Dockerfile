#Pull base image
FROM python:3.10.4-slim-bullseye as builder
# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup app && adduser app --ingroup app
# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/mediafiles
WORKDIR $APP_HOME
# install dependencies


COPY ./requirements.txt .
RUN pip install -r requirements.txt
#Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# copy project
COPY . $APP_HOME
RUN chown -R app:app $APP_HOME
# change to the app user
USER app
#Set work directory


#Install dependencies


