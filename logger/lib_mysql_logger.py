#!/usr/bin/env python3
# -*-
"""
    class Mysql to manage de db access for the programm temp_db
"""
import socket
import sys
from tkinter import messagebox
import os
# if os.name == 'nt':
#     import PyMySQL
# else:
# import mysql.connector
# import pymysql
import mysql.connector

import tkinter as tk
from datetime import datetime, timedelta
import time
import pdb


class Mysql:
    
    """ cette classe sert à accéder à la base de données des températures
        les valeurs sont retournées selon la liste ci-après.
        
        La base de données est sur le RPI 192.168.1.109 et est accessible en local ou par le réseau.
        L'accès à la base de données est vérifiée lors de l'_init et les défauts d'accès sont enregistrés.
        
        ------------------------------------------------------------
        index dans data_from_db et data_for_graph et noms des champs
        ------------------------------------------------------------
        index   db name     designation
        0       t0          from pac
        1       t1          to pac
        2       t2          from accu
        3       t3          on bypass
        4       t4          to home
        5       t5          from home rez
        6       t6          from home 1er
        7       t7          from home
        8       t8          from bypass
        9       t9          to boiler
        10      t10         in boiler
        11      t11         from boiler
        12      t12         salon
        13      t13         bureau
        14      t14         exterieur
        15      s10         pump boiler
        16      s11         pump home
        17      s20         pac on-off
        18      s21         boiler on-off
        19      time_stamp
        20      id
        ------------------------------------------------------------
        
        Procédures :
        _init ()
        get_last_mesured_temperature() -> retourne les dernières temperatures acquises
        get_temp_for_graph() -> retourne les températures sur la plage de temps choisie
        get_temp_to_complete_graph() -> retourne les températures acquises après la dernière mise à jour de l'affichage
    """

    def __init__(self, ip_db_server):
        
        # version infos
        VERSION_NO = "0.01.02" 
        VERSION_DATE = "12.03.2024"
        VERSION_DESCRIPTION = "usage de pymysql à la place de mysql.connector"
        VERSION_STATUS = "en développement "
        VERSION_AUTEUR = "josmet"
        
        self.database_username = "pi"  # YOUR MYSQL USERNAME, USUALLY ROOT
        self.database_password = "mablonde"  # YOUR MYSQL PASSWORD
        self.database_name = "logger"  # YOUR DATABASE NAME
        self.host_name = "localhost"
        self.server_ip = ip_db_server
        self.record = ""
        # get the local IP adress
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.local_ip = s.getsockname()[0]
        s.close()
        # calculate the delay time before retray connection
        ip_s = str(self.local_ip)
        self.delay_time = int(ip_s[-1:])*2 # delay time is different if the ip is differnet so less conflicts
        if self.delay_time == 0 : self.delay_time = 10
        # print(self.delay_time)
        # verify the db connection
        con, e = self.get_db_connection(self.database_name)
        if not con:
            print("mysql_lib_logger : _init_ -> DB UNEXPECTED ERROR\n" + str(e[0]), "/", str(e[1]), "/", str(e[2]) + "\nLe programme va s'arrêter")
            msg = "".join(["ERROR " + str(e[0]), "/ ", str(e[1]), "/ ", str(e[2]) + "Le programme va s'arrêter"])
            tk.messagebox.showerror("mysql_lib_logger ERROR", msg)
            print("DB UNEXPECTED ERROR", msg)
            sys.exit()
            
    def get_db_connection(self, db):
        
        # verify if the mysql server is ok and the db avaliable
        try:
            if self.local_ip == self.server_ip: # if we are on the RPI with mysql server (RPI making temp acquis)
                # test the local database connection
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.host_name, database=db)
#                 con = pymysql.connect(user=self.database_username, password=self.database_password, host=self.host_name, database=self.database_name)
#                 print("".join(['Connected on local DB "', db, '"']))
            else:
                # test the distant database connection
                con = mysql.connector.connect(user=self.database_username, password=self.database_password, host=self.server_ip, database=db)
#                 con = pymysql.connect(user=self.database_username, password=self.database_password, host=self.server_ip, database=self.database_name)
#                 print("".join(['Connected on distant DB "', db, '" on "', self.server_ip, '"']))
            return con, sys.exc_info()
        
        except:
            # return error
            return False, sys.exc_info()
        
    def get_first_mesured_temperature(self):
      
        con, e = self.get_db_connection(self.database_name)
        if not con:
            print("get_last_mesured_temperature -> DB UNEXPECTED ERROR " + str(e) + " Le programme va s'arrêter")
            msg = "DB UNEXPECTED ERROR", " Erreur innatendue " + str(e) + " Le programme va s'arrêter"
            tk.messagebox.showerror(msg)
            exit()
        
        cur = con.cursor()
        sql_txt =  "SELECT time_stamp, t12, t13, t14 FROM tlog WHERE id=(SELECT MIN(id) FROM tlog);"
        cur.execute(sql_txt)
        row = cur.fetchall()
        # return only the first record
        return row[0]
        
    def get_last_mesured_temperature(self):
      
        con, e = self.get_db_connection(self.database_name)
        if not con:
            print("get_last_mesured_temperature -> DB UNEXPECTED ERROR " + str(e) + " Le programme va s'arrêter")
            msg = "DB UNEXPECTED ERROR", " Erreur innatendue " + str(e) + " Le programme va s'arrêter"
            tk.messagebox.showerror(msg)
            exit()
        
        cur = con.cursor()
        sql_txt =  "SELECT time_stamp, t12, t13, t14 FROM tlog WHERE id=(SELECT MAX(id) FROM tlog);"
        cur.execute(sql_txt)
        row = cur.fetchall()
        # return only the first record
        return row[0]

    def get_temp_for_graph(self, nbre_hours_on_graph):
        
        # return the measured temperature for the last "nbre_hours_on_graph"
        
        time_last_mesure = self.get_last_mesured_temperature()[0]  # pour test on prend la dernière valeur de la base de données
        time_last_mesure_str = "".join([str(time_last_mesure.year),"-",str(time_last_mesure.month),"-", str(time_last_mesure.day)," ",
                             str(time_last_mesure.hour),":",str(time_last_mesure.minute),":",str(time_last_mesure.second)]) 

        time_end_mesure = datetime.strptime(time_last_mesure_str, '%Y-%m-%d %H:%M:%S')
        time_begin_mesure = time_end_mesure - timedelta(hours=nbre_hours_on_graph)
        
        first_record_in_db = self.get_first_mesured_temperature()[0]
        
################### modif du 10.08.2020 ############################
# test déplacé dans la procédure refresh_data_and_display()
#
#         if first_record_in_db > time_begin_mesure:
#             msg = "Le premier enregistrement de la base de donnée est plus récent que la date de début désirée.\n\n"
#             msg += "La date de début est donc fixée à la date du premier enregistrement."
#             print(msg)
#             tk.messagebox.showinfo("Plage de données", msg)
#             time_begin_mesure = first_record_in_db
####################################################################

        # connect the db and create the cursor to access the database
        con, e = self.get_db_connection(self.database_name)
        if not con:
            print("get_temp_for_graph -> DB UNEXPECTED ERROR\n" + str(e[0]), "/", str(e[1]), "/", str(e[2]) + " Le programme va s'arrêter")
            msg = "".join(["ERROR " + str(e[0]), "/ ", str(e[1]), "/ ", str(e[2]) + "Le programme va s'arrêter"])
            tk.messagebox.showerror("DB UNEXPECTED ERROR", msg)
            exit()
            
        cur = con.cursor()
        sql_txt = "".join(["SELECT t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, s10, s11, s20, s21, time_stamp, id ",
                           "FROM tlog WHERE time_stamp BETWEEN '", str(time_begin_mesure), "' AND '", str(time_end_mesure), "';"])
        cur.execute(sql_txt)
        row = cur.fetchall()
        
        return row

    def get_temp_to_complete_graph(self, last_id):
        
        connect_try_count = 0
        con = False
        
        while not con:
            
            connect_try_count += 1
            
            # connect the db and return the temperaures not actually on the graph (last_id = last_id on the graph)
            con, e = self.get_db_connection(self.database_name)
            if not con:
                if connect_try_count == 1:
                    msg = "".join([datetime.strftime(datetime.today(), '%d-%m-%Y %H:%M:%S'), " -> Problème de connection sur la db. Le systeme tente de se reconnecter."])
                    print(msg)
                msg = " ".join(["-> Essai no:", str(connect_try_count), ":", str(e[0]), "/", str(e[1])])
                print(msg)
                time.sleep(self.delay_time)

        cur = con.cursor()
        sql_txt = "".join(["SELECT t0, t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12, t13, t14, s10, s11, s20, s21, time_stamp, id ",
                           "FROM tlog WHERE id > '", str(last_id), "';"])
        cur.execute(sql_txt)
        row = cur.fetchall()
        
        return row


if __name__ == '__main__':

    db_server_ip = '192.168.1.108'
    mysql_init = Mysql(db_server_ip)
    ip  = mysql_init.local_ip
    connection = mysql_init.get_db_connection(mysql_init.database_name)
    
    # verify connection
    if connection:
        print("connected on db server on",db_server_ip)
            
        # verify mysql_init.get_last_mesured_temperature()
        data = mysql_init.get_last_mesured_temperature()
        print(" ".join(["function: get_last_mesured_temperature -->", str(datetime.strptime(str(data[0]), '%Y-%m-%d %H:%M:%S')), "salon=",
                        str(data[1]), "bureau=", str(data[2]), "exterieur=", str(data[3])]))
        
        # verify mysql_init.get_temp_for_graph()
        data = mysql_init.get_temp_for_graph(12)
        print(" ".join(["function: get_temp_for_graph -->", str(len(data)), "records received for 12 hours"]))
        
        # verify mysql_init.get_temp_to_complete_graph()
        data = mysql_init.get_temp_to_complete_graph(1)
        print(" ".join(["function: get_temp_to_complete_graph --> there is", str(len(data)), "new records"]))
   
    
    
