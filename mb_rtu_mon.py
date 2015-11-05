#!/usr/bin/env python

# home : https://github.com/sourceperl/modbus-serial-monitor

# modbus/RTU python monitor (check serial frame between devices)

# format modbus RTU serial frame receive from a serial port to console stdout
# check with python2.7 and python3

# synoptic :
#
#   RS-485 bus -> FTDI USB cable ->  /dev/ttyUSBx -> this_script -> CSV modbus
#   RS-422                                                            decode
#   RS-232

# CSV out sample :
# DATE=2015-11-05T17:31:27.977;ERR=NO;FRAME=01-03-50-00-00-04-55-09;SLAVE=1;

# use it like this :
#   - see frame only for slave 17 :
#       $ ./mb_rtu_mon.py | grep SLAVE=0x11
#   - store all traffic on a file
#       $ ./mb_rtu_mon.py > modbus.log

import sys
import serial
import struct
from datetime import datetime

# some const 
DEVICE = '/dev/ttyUSB0'
BAUDRATE = 9600
TIMEOUT = 0.0037 # 3.7ms for 9600 bauds
SEP = ";"

def frame2crc(frame):
    """Compute modbus CRC16 (for RTU mode)

    :param label: modbus frame
    :type label: str (Python2) or class bytes (Python3)
    :returns: CRC16
    :rtype: int
    """
    crc = 0xFFFF
    for index, item in enumerate(bytearray(frame)):
        next_byte = item
        crc ^= next_byte
        for i in range(8):
            lsb = crc & 1
            crc >>= 1
            if lsb:
                crc ^= 0xA001
    return crc

# init serial object
ser = serial.Serial(DEVICE, BAUDRATE)

# serial timeout = modbus end of frame (3.5 * byte tx time)
ser.timeout = TIMEOUT

while True:
    # maximum size of modbus RTU frame is 256 bytes
    frame = ser.read(256)
    # for null size (no data)
    if not frame:
      continue
    # init vars
    err_str = "NO"
    slave_id = 0
    f_code = 0
    e_code = 0
    # add date and time
    now = datetime.now()
    date = now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    # format modbus frame as txt string
    txt_frame = ''
    for item in bytearray(frame):
        if txt_frame:
            txt_frame += "-"
        txt_frame += "%02x" % item
    # check short frame
    if len(frame) >= 5:
        # check CRC
        r_crc = struct.unpack("<H", frame[-2:])[0]
        c_crc = frame2crc(frame[:-2])
        crc_ok = (r_crc == c_crc)
        if not crc_ok:
            err_str = "BAD_CRC"
        else :
            # slave ID
            slave_id = struct.unpack("B", frame[0:1])[0]
            # function code
            f_code = struct.unpack("B", frame[1:2])[0]
            # except code
            if f_code > 0x80:
                err_str = "EXCEPT_FRAME"
                e_code = struct.unpack("B", frame[2:3])[0]
    else:
        err_str = "SHORT_FRAME"
    # out result
    csv_line = ("DATE={0}"+SEP+"ERR={1}"+SEP+"FRAME={2}"+SEP+"SLAVE={3}"+SEP).format(date, err_str, txt_frame, slave_id)
    print(csv_line)
    sys.stdout.flush()
       
ser.close()
