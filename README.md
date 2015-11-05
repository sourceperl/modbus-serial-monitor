# modbus-serial-monitor

modbus/RTU python monitor (check serial frame between devices)

format modbus RTU serial frame receive from a serial port to console stdout
check with python2.7 and python3

synoptic :

  RS-485 bus -> FTDI USB cable ->  /dev/ttyUSBx -> this_script -> CSV modbus
  RS-422                                                            decode
  RS-232

CSV out sample :
DATE=2015-11-05T15:08:25.220;FRAME=11-03-00-00-00-04-46-99;CRC=OK;CRC_VAL=0x9946;SLAVE=0x11;FC=0x03;

use it like this :
  - see frame only for slave 17 :
      $ ./mb_rtu_mon.py | grep SLAVE=0x11
  - store all traffic on a file
      $ ./mb_rtu_mon.py > modbus.log
