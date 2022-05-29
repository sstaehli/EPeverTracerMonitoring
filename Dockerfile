FROM python:latest

RUN pip3 install minimalmodbus influxdb configparser

COPY modules/ modules/
COPY influx.db influx.db
COPY logtracer.py logtracer.py

RUN mkdir -p log/

CMD [ "python" , "logtracer.py", "1", "pvvolt"]