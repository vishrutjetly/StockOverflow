FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
RUN apt-get install default-libmysqlclient-dev
ADD . /code/
EXPOSE 8000
COPY .env.docker .env