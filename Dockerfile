FROM nikolaik/python-nodejs:python3.9-nodejs17
RUN apt-get update && apt-get upgrade -y
RUN apt-get install ffmpeg -y
COPY . /app/
WORKDIR /app/
RUN pip3 install -U pip
RUN pip3 install -U -r installer
CMD python3 -m vexera.py