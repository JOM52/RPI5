#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
logger.py
reading and saving data from temperature sensors ds18b20 ans state sensors ds2413
written by Joseph Metrailler in 2016-2018-2020 (parts of code from Adafruit).

--> Acquisition des températures et  états puis enregistrement dans la base de données 
    exécuté à chaque minute 24/24 365/365
    13.08.2020 -> version 1.0.0 -> en service sans problème depuis 3 mois
"""

from lib_ds18b20_logger import DS18B20 # import class DS18B20
from lib_ds2413_logger import DS2413 # import class DS2413
from lib_mysql_logger import Mysql # import Mysql class

import time
import datetime
from tkinter import messagebox
import sys
# import mysql.connector

class DataLogger:
    
    def __init__(self):
        
        # version infos
        VERSION_NO = "1.0.0" 
        VERSION_DATE = "13.08.2020"
        VERSION_DESCRIPTION = "en service sans problème depuis 3 mois"
        VERSION_STATUS = "ok"
        VERSION_AUTEUR = "josmet"
        
        # init times
        self.v_time_start = time.strftime('%Y.%m.%d %H:%M:%S') # to save start time
        self.v_time_begin = time.time() # to calculate elapsed tiem

        # initialise database access
        mysql_ip = "192.168.1.165"
        db_name = "logger"
        self.mysql_con = Mysql(mysql_ip)

        # initialise temperature sensors
        self.ds18b20_array = DS18B20()
        self.nbre_ds18b20 = self.ds18b20_array.device_count()

        # initialise state sensors
        self.ds2413_array = DS2413()
        self.nbre_ds2413 = self.ds2413_array.device_count()
        
        # check count_wireless_sensors
#         self.nbre_wireless_ds18b20 = self.count_wireless_ds18b20()
        
        # no connected sensor -> exit
        if self.nbre_ds18b20 == 0 and self.nbre_ds2413 == 0: # and self.nbre_wireless_ds18b20 == 0:
            msg = "Aucun capteur détecté. Ajoutez des capteurs de température DS18B20 ou d'état DS2413 ou wireless puis relancez le programme."
            title = "Sensors_ERROR"
            print(msg)
            messagebox.showerror(title, msg)
            sys.exit()

        elif self.nbre_ds2413 == 0:
            msg = "Pas de capteurs on/off détectés. L'acquisition se poursuit sans mesure d'état"
            title = "DS2413 ERROR"
            print(msg)

        elif self.nbre_ds18b20 == 0:
            msg = "Pas de capteurs de température détectés. L'acquisition se poursuit sans mesure de température cablée"
            title = "DS18B20 wired ERROR"
            print(msg)

#         elif self.nbre_wireless_ds18b20 == 0:
#             msg = "Pas de capteurs de température wireless détectés. L'acquisition se poursuit sans mesure de température wireless"
#             title = "DS18b20 wireless ERROR"
#             print(msg)
            
        msg = "".join([str(self.nbre_ds18b20), " capteurs de température DS18B20 cablés détecté(s)\n",
                       # str(self.nbre_wireless_ds18b20), " capteurs de température DS18B20 sans fil détecté(s)\n",
                       str(self.nbre_ds2413), " capteurs d'état détecté(s)"])
        print(msg)

#     def count_wireless_ds18b20(self):
#         
#         n_ds18x20_sensors = 0
#         sql_txt = "SELECT sensorid, sensorval FROM reduit"
#         reduit_connection, err = self.mysql_con.get_db_connection("mqtt")
#         print('reduit_connection:', reduit_connection, 'err:', err)
#         reduit_cursor = reduit_connection.cursor()
#         reduit_cursor.execute(sql_txt)
#         reduit_row = reduit_cursor.fetchall()
#         n_ds18x20_sensors = len(reduit_row)
#         reduit_cursor.close()
#         reduit_connection.close()
#         return n_ds18x20_sensors
# 
#     def get_wireless_temp(self):
#         
#         try:
#             temp_reduit =[]
#             
#             sql_txt = "SELECT sensorid, sensorval FROM reduit"
#             reduit_connection, err = self.mysql_con.get_db_connection("mqtt")
#             reduit_cursor = reduit_connection.cursor()
#             reduit_cursor.execute(sql_txt)
#             reduit_row = reduit_cursor.fetchall()
#             reduit_cursor.close()
#             reduit_connection.close()
#             
#             db_connection, err = self.mysql_con.get_db_connection("logger")
#             for row in reduit_row:
#                 sensor_id = row[0].strip()
#                 sensor_temp = row[1]
#                 sql_txt = "SELECT id, sensor_txt FROM tsensor WHERE sensor_id = '" + sensor_id + "'"
#                 db_cursor = db_connection.cursor()
#                 db_cursor.execute(sql_txt)
#                 row= db_cursor.fetchall()
#                 if len(row) > 0:
#                     table_id = row[0][0]
#                     sensor_txt = row[0][1]
#                     temp_reduit.append([table_id, sensor_id, sensor_txt, sensor_temp])
#             db_cursor.close()
#             db_connection.close()
#             return temp_reduit
#         except:
#             return -333

    def run_acquis(self):
        
        # temperatures reduit
        temp_reduit =[]
        temp_reduit = -333 #self.get_wireless_temp()
        print("---------------------------------------------------------------")
        if temp_reduit != -333:
            for z in temp_reduit:
                table_id = z[0]
                sensor_id = z[1]
                sensor_txt = z[2]
                sensor_temp = z[3]
                print("".join([str(table_id) + ' - ' + str(sensor_id) + ' -> ' + sensor_txt + ' = ' + str(sensor_temp)]))
        else:
            print('no reduit data availlable')
        print("---------------------------------------------------------------")
            
        # autres températures
        db_connection, err = self.mysql_con.get_db_connection("logger")
        pass_count = 1
        if not db_connection :
            while pass_count > 0:
                db_connection, err = self.mysql_con.get_db_connection(False)
                if not db_connection:
                    pass_count -= 1
                else:
                    pass_count = 0
            if not db_connection:
                msg = "".join(["DB connection error ", err])
                print(msg)
                title = "DB error"
                messagebox.showerror(title, msg)
                sys.exit()
            
        db_cursor = db_connection.cursor()
        
        nbre_max_temp_sensors = 30
        ds18b20_ids = [0] * nbre_max_temp_sensors 
        ds18b20_temp = [-333] * nbre_max_temp_sensors

        #for each existing temperature sensor
        for i in range(self.nbre_ds18b20):
            
            t_start_boucle = time.time()
            mesure_ok = True # the logic to check the validity of the data and record or not the mesure

            # read the sensors : temperature, id and status 
            temperature, sensor_id, mesure_status = self.ds18b20_array.tempC(i)
            if mesure_status != 'ok':
                temperature = -333

            # get the sensor infos
            sql_txt = "".join(["SELECT sensor_no, sensor_field, sensor_txt FROM tsensor WHERE sensor_id='",sensor_id, "'"])
            db_cursor.execute(sql_txt)
            rows = db_cursor.fetchall()
            if len(rows) > 0: # the sensor exist in DB
                sensor_num = int(rows[0][0])
                sensor_field = rows[0][1]
                sensor_txt = rows[0][2]
            else: # the sensor dont exist in DB so add it
                # find the first free place for ds18b20 in sensor table
                sql_txt = "select sensor_no, sensor_field from tsensor where sensor_type='ds18b20' and sensor_id='' order by sensor_field limit 1;"
                db_cursor.execute(sql_txt)
                rows = db_cursor.fetchall()
                if len(rows) > 0:
                    sensor_num = int(rows[0][0])
                    sensor_field = rows[0][1]

                    # New sensor found what to do with that ?
                    print("Found a new sensor with the id " + sensor_id)
                    v_answer = input("Do you want to add it in the database Y/N ? ").lower()

                    if str(v_answer) == "y": # y then ask for the name of this new sensor
                        sensor_txt = input("What name do you want for this new sensor ? (default value = New sensor " + str(sensor_field) + ")")
                        if len(sensor_txt) == 0 :
                            sensor_txt = "New sensor " + str(sensor_field)
                        sensor_num = rows[0][0]
                        sensor_field = rows[0][1]
                        
                        # add the new sensor in the database
                        sql_txt = "".join(["UPDATE tsensor SET sensor_id='", sensor_id, "', sensor_txt='", sensor_txt, "' WHERE sensor_no=", str(sensor_num), ";"])
                        db_cursor.execute(sql_txt)
                        db_connection.commit()
                        
                    else :
                        mesure_ok = False # do not record any value for this sensor
                else:
                    msg = "Plus possible d'ajouter des capteurs de température."
                    title = "Sensors_ERROR"
                    print(msg)
                    mesure_ok = False

            # traite les erreurs les plus fréquentes soit temp = 85°C
            pass_count = 1
            if temperature >= 85:
                while pass_count > 0:
                    temperature, sensor_id, mesure_status = self.ds18b20_array.tempC(i)
                    txt = "".join([time.strftime('%Y.%m.%d %H:%M:%S'), " Capteur : ", str(sensor_num), " --> temperature = 85°C --> essai no : ", str(pass_count)])
                    print(txt)
                    if temperature >= 85:
                        pass_count -= 1
                        if pass_count == 0:
                            txt = "".join([time.strftime('%Y.%m.%d %H:%M:%S'), " Capteur : ", str(sensor_num), " --> temperature = 85°C --> essai no : ", str(pass_count)])
                            print(txt)
                            mesure_status = "Erreur de mesure"
                            mesure_ok = False

                            sys.stdout.write("\033[1;31m") # blue = "\033[1;34m" -> red = "\033[1;31m" --> green = "\033[0;32m"
                            print(str(sensor_num) + ' - ' + str(sensor_id) + ' -> ' + sensor_txt + ' = ' + str(temperature) + ' --> ' + mesure_status)
                            sys.stdout.write("\033[0m") # end color
                    else:
                        pass_count = 0
                                          
            if mesure_ok:
                sensor_num1 = sensor_num 
                # save the temperature and sensorId in arrays
                ds18b20_ids[sensor_num1] = sensor_id
                ds18b20_temp[sensor_num1] = temperature # t2
                print("".join([str(sensor_num1+1) + ' - ' + str(ds18b20_ids[sensor_num1]) + ' -> ' + sensor_txt + ' = ' + str(ds18b20_temp[sensor_num1])
                               + ' -> ' + mesure_status, " -> elapsed ", '{0:.2f}'.format(time.time() - t_start_boucle), "s"]))

        # temperatures reduit


        # State sensors
        
        print()
        nbre_max_state_sensors = 3
        ds2413_ids = ['spare'] * nbre_max_state_sensors * 2
        ds2413_states = [-1] * nbre_max_state_sensors * 2
        
        for index in range (self.nbre_ds2413):
            
            PIO = [-1] * 2
            PIO[0], PIO[1], sensor, status = self.ds2413_array.read_ds2413(index)
            
            if status == 'ok':
                for chanel in range(2):
                    sql_txt = "".join(["select sensor_txt from tsensor where sensor_type='ds2413' and sensor_id='",
                                       sensor, "' and sensor_chanel='", str(chanel), "';"])         
                    db_cursor.execute(sql_txt)
                    rows = db_cursor.fetchall()
                    if len(rows) > 0: # the sensor exist in DB
                        sensor_txt = rows[0][0]
                        
                        ds2413_ids[index * 2 + chanel] = sensor_txt
                        ds2413_states[index * 2 + chanel] = PIO[chanel]
                        
                    else: # the sensor dont exist in DB so add it
                        print("rows = 0")
                        pass
            else:
                print("".join([datetime.datetime.now().strftime("%Y.%m.%d, %H:%M:%S"), "\n", sensor, " -> ", status]))
                pass
        # print the status of states sensors
        for i in range (4):
            print(ds2413_ids[i], ds2413_states[i])
        print()

        print("save the results in the database")
#         sql_txt = " ".join([
#             "INSERT INTO tlog (t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, s10, s11, s20, s21, s30, s31) VALUES (", 
#              str(ds18b20_temp[0]),",",str(ds18b20_temp[1]),",",str(ds18b20_temp[2]),",",str(ds18b20_temp[3]),",",str(ds18b20_temp[4]),",",str(ds18b20_temp[5]),",",
#              str(ds18b20_temp[6]),",",str(ds18b20_temp[7]),",",str(ds18b20_temp[8]),",",str(ds18b20_temp[9]),",",str(ds18b20_temp[10]),",",
#              str(ds18b20_temp[11]),",",str(ds18b20_temp[12]),",",str(ds18b20_temp[13]),",",str(ds18b20_temp[14]),",",str(ds18b20_temp[15]),",",
#              str(ds18b20_temp[16]),",",str(ds18b20_temp[17]),",",str(ds18b20_temp[18]),",",str(ds18b20_temp[19]),",",str(ds18b20_temp[20]),",",
#              str(ds2413_states[0]),",",str(ds2413_states[1]),",",str(ds2413_states[2]),",",str(ds2413_states[3]),",",str(ds2413_states[4]),",",str(ds2413_states[5]),")"])
        if temp_reduit != -333:
            sql_txt = " ".join([
                "INSERT INTO tlog (t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, s10, s11, s20, s21, s30, s31) VALUES (", 
                 str(ds18b20_temp[0]),",",str(ds18b20_temp[1]),",",str(ds18b20_temp[2]),",",str(ds18b20_temp[3]),",",str(ds18b20_temp[4]),",",str(ds18b20_temp[5]),",",
                 str(ds18b20_temp[6]),",",str(ds18b20_temp[7]),",",str(ds18b20_temp[8]),",",str(ds18b20_temp[9]),",",str(ds18b20_temp[10]),",",
                 str(ds18b20_temp[11]),",",str(ds18b20_temp[12]),",",str(ds18b20_temp[13]),",",str(ds18b20_temp[14]),",",str(temp_reduit[1][3]),",",
                 str(temp_reduit[0][3]),",",str(ds18b20_temp[17]),",",str(ds18b20_temp[18]),",",str(ds18b20_temp[19]),",",str(ds18b20_temp[20]),",",
                 str(ds2413_states[0]),",",str(ds2413_states[1]),",",str(ds2413_states[2]),",",str(ds2413_states[3]),",",str(ds2413_states[4]),",",str(ds2413_states[5]),")"])
        else:
            sql_txt = " ".join([
                "INSERT INTO tlog (t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, t15, t16, t17, t18, t19, t20, s10, s11, s20, s21, s30, s31) VALUES (", 
                 str(ds18b20_temp[0]),",",str(ds18b20_temp[1]),",",str(ds18b20_temp[2]),",",str(ds18b20_temp[3]),",",str(ds18b20_temp[4]),",",str(ds18b20_temp[5]),",",
                 str(ds18b20_temp[6]),",",str(ds18b20_temp[7]),",",str(ds18b20_temp[8]),",",str(ds18b20_temp[9]),",",str(ds18b20_temp[10]),",",
                 str(ds18b20_temp[11]),",",str(ds18b20_temp[12]),",",str(ds18b20_temp[13]),",",str(ds18b20_temp[14]),",",'-333',",",
                 '-333',",",str(ds18b20_temp[17]),",",str(ds18b20_temp[18]),",",str(ds18b20_temp[19]),",",str(ds18b20_temp[20]),",",
                 str(ds2413_states[0]),",",str(ds2413_states[1]),",",str(ds2413_states[2]),",",str(ds2413_states[3]),",",str(ds2413_states[4]),",",str(ds2413_states[5]),")"])
        db_cursor.execute(sql_txt)
        db_connection.commit()
        db_cursor.close()
        db_connection.close()

if __name__ == '__main__':
    
    data_logger = DataLogger()
    data_logger.run_acquis()
