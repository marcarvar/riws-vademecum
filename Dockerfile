FROM ubuntu:latest

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip 

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt


COPY ./entrypoint.sh .
RUN chmod 777 entrypoint.sh



ENTRYPOINT ["./entrypoint.sh"]
