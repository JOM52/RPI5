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
# ds2413.py written by Joseph Metrailler

import os
import glob
import time
import numpy
import sys
import datetime

class DS2413:
   
    def __init__(self):

        # load required kernel modules
        os.system('sudo modprobe w1-gpio')
        os.system('sudo modprobe w1-ds2413')

        # Find file names for the sensor(s)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '3a*')
        self._num_devices = len(device_folder)
        self._device_file : list = [] 
        
        for i in range(self._num_devices):
            self._device_file.append(device_folder[i] + '/state')
            
    def _read_ds2413(self,index):
        # you should not call this directly
        try:
            with  open(self._device_file[index],'rb') as f:
                pass
        except FileNotFoundError:
            self.__init__()
        except:
            return 999 , "error", "DS2413 sensor missing, sensor list is reset"
            
        sensor_path = self._device_file[index]
        sensor_no = sensor_path.split('/')
        sensor = sensor_no[5]
        with  open(self._device_file[index],'rb') as f:
            try:
                ds_status = f.read()
            except OSError:
                sensor_ok = False
                return 999 , sensor, "DS2413 error: sensor not found"
            except:
                return 999 , sensor, "DS2413 error: reset sensor list"

            sensor_byte = numpy.fromfile(self._device_file[index], dtype = "uint8")
            sensor_bits = numpy.unpackbits(sensor_byte)

            # DS2413 bits map
            # bits[7] -> PIOA pin state
            # bits[6] -> PIOA latch state
            # bits[5] -> PIOB pin state
            # bits[4] -> PIOB latch state
            # bits[3] -> bits[7] inverted
            # bits[2] -> bits[6] inverted
            # bits[1] -> bits[5] inverted
            # bits[0] -> bits[4] inverted
            
        return sensor_bits, sensor, "ok"
      
    def read_ds2413(self,index = 0):
        # detected by a sensor
        sensor_bits, sensor, status = self._read_ds2413(index)
        retries = 1
        while (status != 'ok') and (retries > 0):
            # read failed so try again
            time.sleep(0.1)
            ds_status, sensor, status = self._read_ds2413(index)
            retries -= 1
        if retries == 0:
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
        print("error: no DS2413 found")
        sys.exit(0)
        
    for i in range(ds2413._num_devices):
        PIOA, PIOB, sensor, status = ds2413.read_ds2413(i)
        if status == 'ok':
            print("".join([sensor, " PIOA=", str(PIOA), " PIOB=", str(PIOB), " ", status]))
        else:
            print("".join([datetime.datetime.now().strftime("%Y.%m.%d, %H:%M:%S"), "\n", sensor, " -> ", status]))


