import pandas as pd
import numpy as np
import sys
import os
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))[:-3] + "\\cfg")
from config import info, debug, warning, log_config, PATH

log_config("proprocess_data")

info('Preprocess Data')

class Preprocessing:

    def __init__ (self, name):
        self.name = name
        self.data_path = "C:/Users/33660/Desktop/Etudes/Master_2/SEMESTRE_1/GENIE LOGICIEL/Projet/Database_Exploitation/data/Consommation/" + name
        self.data = pd.read_excel(self.data_path)

    def drop_column (self, column):
        for i in column:
            self.data = self.data.drop(i, axis=1)
            info(f'column {i} supprimée')

    def drop_line (self, column_interst):
        self.data = self.data.dropna(axis=0, subset=[column_interst])
        info(f'ligne supprimée')

    def save_file (self):
        self.data.to_excel(PATH + '\\data\\output\\' + self.name)
        print("fichier sauvegardée après pre-traitement")
        info('fichier sauvegardée après pre-traitement')




