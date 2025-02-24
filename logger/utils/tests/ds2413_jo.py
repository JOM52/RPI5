#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Much of this code is lifted from Adafruit web site for DS18B20 temperature sensor
   Adaptation for DS2413 written by Joseph Metrailler april 2020
   
   This class can be used to access one or more DS2413 1-wire dual channel adressable switch
   It uses OS supplied drivers and one wire 
   
   To do this add the line dtoverlay=w1-gpio to the end of /boot/config.txt
   
   The DS12413 transmit over 1wiew connection 2 on-off chanels
   You can connect more than one sensor to the same set of pins
   Only one pullup resistor is required
"""
# ds18b20.py written by Roger Woollett
# ds2413 .py written by Joseph Metrailler

import os
import glob
import time
import numpy
import sys

class DS2413:

   
    def __init__(self):

        # load required kernel modules
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-ds2413')

        # Find file names for the sensor(s)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '3a*')
        self._num_devices = len(device_folder)
        self._device_file = [] 
        i = 0
        while i < self._num_devices:
            self._device_file.append(device_folder[i] + '/state')
            i += 1
            
    def _read_ds2413(self,index):
        # you should not call this directly
        with  open(self._device_file[index],'rb') as f:
            try:
                ds_status = f.read()
            except OSError:
                sensor_ok = False
#                 print("OS error: {0}".format(sys.exc_info()[0]))
                return 999 , "xxx", "error: sensor not found"
            except:
#                 print("Unexpected error:", sys.exc_info()[0])
                return 999 , "xxx", "unexpected error"

            sensor_path = self._device_file[index]
            sensor_no = sensor_path.split('/')
            sensor = sensor_no[5]
            sensor_byte = numpy.fromfile(self._device_file[index], dtype = "uint8")
            sensor_bits = numpy.unpackbits(sensor_byte)
            
#             if Bits[3] == 1:
#                 PIO1A = "ON"
#             else:
#                 PIO1A = "OFF"
#             if Bits[1] == 1:
#                 PIO1B = "ON"
#             else:
#                 PIO1B = "OFF"
#             
#             print("".join(["sensor:", sensor, " PIOA:", PIO1A]))
#             print("".join(["sensor:", sensor, " PIOB:",PIO1B]))
                
        return sensor_bits, sensor, "ok"
      
    def read_ds2413(self,index = 0):
        # detected by a sensor
        sensor_bits, sensor, status = self._read_ds2413(index)
        retries = 2
        while (status != 'ok') and (retries > 0):
            # read failed so try again
            time.sleep(0.1)
#             print('Read Failed', retries)
            ds_status, sensor, status = self._read_ds2413(index)
            retries -= 1
        if retries == 0:
#             os.system('sudo modprobe w1-gpio')
#             os.system('sudo modprobe w1-ds2413')
            return 0, 0, sensor ,status

        PIOA = sensor_bits[3]
        PIOB = sensor_bits[1]
        return PIOA, PIOB, sensor, status
         
    def device_count(self):
        # call this to see how many sensors have been detected
        return self._num_devices

if __name__ == '__main__':

    ds2413 = DS2413()
    print("Number devices:", ds2413._num_devices)
    if ds2413._num_devices == 0:
        print("error: sensor DS2413 not found")
        exit
        
    while True:
        for i in range(ds2413._num_devices):
            PIOA, PIOB, sensor, status = ds2413.read_ds2413(i)
            if status == 'ok':
                print(sensor, "PIOA", PIOA, "PIOB", PIOB, status)
            else:
                print(sensor, status)
        time.sleep(5)
        print()


