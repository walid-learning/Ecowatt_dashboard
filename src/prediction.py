
import pandas as pd

import sys
import os
import mysql.connector
sys.path.append( os.path.dirname(os.path.abspath(__file__))[:-3] + "\\cfg")
from config import PATH, info, warning, debug
import numpy as np

pd.set_option('display.max_columns', None)

pd.set_option('display.max_rows', None)



# btc = web.get_data_yahoo(['Consommation'], start=datetime.datetime(2015, 1, 1), end=datetime.datetime(2022, 11, 13))['Close']

# print(btc.head())

# btc.to_csv("btc.csv")


# ------------------
mydb = mysql.connector.connect(
host="localhost",
user="root",
database = "ecowatt",
password="Walidluxe99."
)

info('Connexion à la DB OK')

btc = pd.read_sql("""SELECT consommation.Perimetre,CONCAT(SUBSTR(consommation.Date,4,2), "/" ,SUBSTR(consommation.Date,1,2), "/" ,SUBSTR(consommation.Date,7)) as Date, 
                        AVG(Consommation) as Consommation
                        FROM consommation inner join echanges on 
                        (consommation.Perimetre = echanges.Territoire and consommation.Date = echanges.Date
                        and consommation.Heures = echanges.Heures)
                        Group by Date
                        HAVING SUBSTR(Date,7) = 2016
                        ORDER BY Date    ;""", mydb)

#btc = pd.read_csv(PATH + "\\src\\Consommation_2016.csv")

# print(btc.head())

btc.index = pd.to_datetime(btc['Date'], format="%m/%d/%Y")

del btc['Date']

import matplotlib.pyplot as plt

import seaborn as sns

sns.set()

plt.ylabel('Consommation')

plt.xlabel('Date')

plt.xticks(rotation=45)

plt.plot(btc.index, btc['Consommation'] )

# Splitting Data for Training and Testing

train = btc[btc.index < pd.to_datetime("10/01/2016", format="%m/%d/%Y")]

test = btc[btc.index > pd.to_datetime("10/01/2016", format="%m/%d/%Y")]
# train = np.array(train)
# exit()

plt.plot(train['Consommation'], color = "black")


plt.plot(test['Consommation'], color = "red")

plt.ylabel('Consommation (MW)')

plt.xlabel('Date')

plt.xticks(rotation=45)

plt.title("Prédiction de la consommation d'énergie pour les derniers mois de l'année")

#Autoregressive Moving Average (ARMA)

from statsmodels.tsa.statespace.sarimax import SARIMAX

y = train['Consommation']

ARMAmodel = SARIMAX(y, order = (1, 0, 1))

ARMAmodel = ARMAmodel.fit()

y_pred = ARMAmodel.get_forecast(len(test.index))

y_pred_df = y_pred.conf_int(alpha = 0.05) 

y_pred_df["Predictions"] = ARMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])

y_pred_df.index = test.index

y_pred_out = y_pred_df["Predictions"] 

plt.plot(y_pred_out, color='green', label = 'Predictions')

plt.legend()

plt.show()

# We can evaluate the performance using the root mean-squared error

import numpy as np

from sklearn.metrics import mean_squared_error

arma_rmse = np.sqrt(mean_squared_error(test["Consommation"].values, y_pred_df["Predictions"]))

print("RMSE: ",arma_rmse)

#Autoregressive Integrated Moving Average (ARIMA)

from statsmodels.tsa.arima.model import ARIMA

ARIMAmodel = ARIMA(y, order = (2, 2, 2))

ARIMAmodel = ARIMAmodel.fit()

y_pred = ARIMAmodel.get_forecast(len(test.index))

y_pred_df = y_pred.conf_int(alpha = 0.05) 

y_pred_df["Predictions"] = ARIMAmodel.predict(start = y_pred_df.index[0], end = y_pred_df.index[-1])

y_pred_df.index = test.index

y_pred_out = y_pred_df["Predictions"] 

plt.plot(y_pred_out, color='Yellow', label = 'ARIMA Predictions')

plt.legend()