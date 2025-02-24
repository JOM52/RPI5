#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
   Much of this code is lifted from Adafruit web site
   This class can be used to access one or more DS18B20 temperature sensors
   It uses OS supplied drivers and one wire support must be enabled
   
   To do this add the line dtoverlay=w1-gpio to the end of /boot/config.txt
   
   The DS18B20 has three pins, looking at the flat side with the pins pointing
   down pin 1 is on the left
   connect pin 1 to GPIO ground
   connect pin 2 to GPIO 4 *and* GPIO 3.3V via a 4k8 (4800 ohm) pullup resistor
   connect pin 3 to GPIO 3.3V
   You can connect more than one sensor to the same set of pins
   Only one pullup resistor is required
"""
# ds18b20.py
# written by Roger Woollett

import os
import glob
import time
import sys
from math import *

class DS18B20:

   
    def __init__(self):

        # load required kernel modules
        os.system('modprobe w1-gpio')
        os.system('modprobe w1-therm')

        # Find file names for the sensor(s)
        base_dir = '/sys/bus/w1/devices/'
        device_folder = glob.glob(base_dir + '28*')
        self._num_devices = len(device_folder)
        self._device_file = []
        for i in range(self._num_devices):
#         i = 0
#         while i < self._num_devices:
            self._device_file.append(device_folder[i] + '/w1_slave')
#             i += 1
            
    def _read_temp(self,index):
        # Issue one read to one sensor
        # you should not call this directly
        with  open(self._device_file[index],'r') as f:
            lines = f.readlines()
            sensorPath = self._device_file[index]
            sensorNo = sensorPath.split('/')
            sensor = sensorNo[5]
        return lines,sensor
      
    def tempC(self,index = 0):
        # call this to get the temperature in degrees C
        # detected by a sensor
        lines,sensor = self._read_temp(index)
        retries = 2
        while (lines[0].strip()[-3:] != 'YES') and (retries > 0):
            # read failed so try again
            time.sleep(0.1)
#             print('Read Failed', retries)
            lines,sensor = self._read_temp(index)
            retries -= 1
         
        if retries == 0:
            return -333, sensor ,'error: sensor not found'
         
        equals_pos = lines[1].find('t=')
        if equals_pos != -1:
            temp = lines[1][equals_pos + 2:]
            temp = float(temp)/1000
            temp = floor(temp*100)/100
            return temp, sensor, 'ok'
        else:
            # error
            return 999,'','data transmition between sensor and PI error'
         
    def device_count(self):
        # call this to see how many sensors have been detected
        return self._num_devices
    
if __name__ == '__main__':
    
    ds18b20 = DS18B20()
    
    nbre_sensor = ds18b20.device_count()
    print("Number sensors:", nbre_sensor)
    if nbre_sensor == 0:
        print("error: no DS18B20 found")
        sys.exit(0)
        
    for i in range(nbre_sensor):
        temp, sensor, ok = ds18b20.tempC(i)
        print("".join(["Sensor:", sensor, " temp:", str(temp), " ", ok]))

