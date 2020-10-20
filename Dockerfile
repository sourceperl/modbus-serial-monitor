FROM python:3.8-buster

RUN apt-get update && \
    apt-get install -y git python3-setuptools

RUN git clone https://github.com/sourceperl/modbus-serial-monitor.git

WORKDIR /modbus-serial-monitor

RUN python3 setup.py install

ENV DEVICE=/dev/ttyAP0
ENV BAUDRATE=115200

CMD ["sh", "-c", "python3 scripts/modbus-scan-serial --device=$DEVICE --baudrate=$BAUDRATE --parity=N"]

