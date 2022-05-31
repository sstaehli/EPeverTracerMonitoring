FROM python:latest

RUN pip3 install minimalmodbus influxdb_client

COPY modules/ modules/

WORKDIR /upowerlog/

RUN mkdir -p log/

CMD [ "python" , "upowerlog.py" ]