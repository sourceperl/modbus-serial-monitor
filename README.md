modbus-serial-monitor
=====================

Modbus/RTU python monitor: check serial frame between devices.

Format modbus RTU serial frames receive from a serial port to console stdout.

Test with python2.7 and python3.

## Synoptic

    RS-485 
    RS-422 bus  -> FTDI cable ->  /dev/ttyUSBx -> this_script -> CSV out
    RS-232

## CSV out sample

DATE=2015-11-05T17:31:27.977;ERR=NO;FRAME=01-03-50-00-00-04-55-09;SLAVE=1;

## Use it

See frame only for slave 1

    $ ./mb_rtu_mon.py | grep SLAVE=1

Store all traffic on modbus.log file

    $ ./mb_rtu_mon.py > modbus.log
