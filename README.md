modbus-serial-monitor
=====================

Modbus/RTU python monitor: check serial frame between devices.

Format modbus RTU serial frames receive from a serial port to console stdout.

Test with python3.

## Synoptic

    RS-485 
    RS-422 bus  -> FTDI cable ->  /dev/ttyUSBx -> this_script -> CSV out
    RS-232

## CSV out sample

DATE=2015-11-05T17:31:27.977;ERR=NO;FRAME=01-03-50-00-00-04-55-09;SLAVE=1;

## Prerequisite 

E.g. in Debian based dists, install package:

    $ sudo apt-get install python3-setuptools

## Setup

    $ sudo python3 setup.py install

## Use it

Help

    $ modbus-scan-serial -h

See frame only for slave 1

    $ modbus-scan-serial -d /dev/ttyUSB2 | grep SLAVE=1

Store all traffic on modbus.log file

    $ modbus-scan-serial > modbus.log

