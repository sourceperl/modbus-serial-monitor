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
# DATE=2015-11-05T15:08:25.220;FRAME=11-03-00-00-00-04-46-99;CRC=OK; /
# CRC_VAL=0x9946;SLAVE=0x11;FC=0x03;

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
ser.timeout = (10.0/ser.baudrate) * 3.5

while True:
    # maximum size of modbus RTU frame is 256 bytes
    frame = ser.read(256)
    # for null size (no data)
    if not frame:
      continue
    # csv line output
    csv_line = ''
    # add date and time
    now = datetime.now()
    csv_line += "DATE=" + now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + SEP
    # format modbus frame as txt string
    txt_frame = ''
    for item in bytearray(frame):
        if txt_frame:
            txt_frame += "-"
        txt_frame += "%02x" % item
    csv_line += "FRAME=" + txt_frame + SEP
    # check short frame
    if len(frame) >= 5:
        # check CRC
        r_crc = struct.unpack("<H", frame[-2:])[0]
        c_crc = frame2crc(frame[:-2])
        crc_ok = (r_crc == c_crc)
        if crc_ok:
            csv_line += "CRC=OK" + SEP
        else:
            csv_line += "CRC=KO" + SEP
        csv_line += "CRC_VAL=0x%04x" % c_crc + SEP
        # slave ID
        slave_id = struct.unpack("B", frame[0:1])[0]
        csv_line += "SLAVE=0x%02x" % slave_id + SEP
        # function code
        f_code = struct.unpack("B", frame[1:2])[0]
        csv_line += "FC=0x%02x" % f_code + SEP
    else:
        csv_line += "ERROR='short frame'" + SEP

    print(csv_line)
    sys.stdout.flush()
       
ser.close()
