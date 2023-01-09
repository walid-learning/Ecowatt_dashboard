import sqlite3
import numpy as np 
import csv
import pathlib
import pandas as pd
import mysql.connector
import sys
import os
sys.path.append( os.path.dirname(os.path.abspath(__file__))[:-3] + "\\cfg")
from config import PATH, info, warning, debug

""" This file aims to us to manipulate our database. We will have methods that Select, Update or delete data from The database """

path = str(pathlib.Path(__file__).parent.resolve())
cible_path = path[:-3] + 'data\\'

class Database : 

    def __init__(self, host, user, database, auth_plugin) :
        self.host = host
        self.user = user
        
        self.database = database
        self.auth_plugin = auth_plugin


    def connect(self,passwd):
        self.passwd = passwd
        try :
            myDB = mysql.connector.Connect(
                host = self.host,
                user = self.user,
                passwd = self.passwd,
                database = self.database,
                auth_plugin = self.auth_plugin
            )
            info('Connexion réussie')
            return 'Connexion réussie', True
        except:
            debug ('mot de passe incorrect')
            return 'mot de passe incorrect', False

    def getValue (self, option, jour, mois):
        myDB = mysql.connector.Connect(
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            database = self.database,
            auth_plugin = self.auth_plugin
        )
        cursor = myDB.cursor()
        if option =='heure':
            cursor.execute(f"SELECT Consommation from Echanges where Date == 2018-{mois}-{jour}")
            info("query SQL OK")
            res = cursor.fetchall()
            conso_h = []
            for x in res:
                x = np.array(x)
                conso_h.append(int(x[0]))
            info("consommation horraire envoyée")
            return conso_h
        
        if option =="jour":
            cursor.execute(f"SELECT AVG(Consommation) from Echanges where left(Date,7) == 2018-{mois} group by Date limit 20")
            info("query SQL OK")
            res = cursor.fetchall()
            conso_j = []
            for x in res:
                x = np.array(x)
                conso_j.append(int(x[0]))
            info("consommation journalière envoyée")
            return conso_j




