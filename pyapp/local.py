import os
import sys
from hdbcli import dbapi
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


conn_data = {
    'server' : 'oktnb132.inf.elte.hu',
    'port': 30015,
    'user': 'PY_TU',
    'password': os.environ.get('PY_PASS')
}

conn = dbapi.connect(conn_data['server'], conn_data['port'], conn_data['user'], conn_data['password'])

cursor = conn.cursor()
#cursor.execute("select CURRENT_UTCTIMESTAMP from DUMMY", {})
cursor.execute('select measure_ts, sum(confirmed) confirmed from "COVID_VISUAL_HDI_DB_1"."COVID_visual.db.data::COVIDTIMESERIES" where region like \'%China%\' group by measure_ts order by measure_ts;')
res = cursor.fetchall()
cursor.close()
conn.close()

dt = np.dtype(np.unicode_, 16)

n = np.array([tuple(i) for i in res], np.dtype([
  ("f2", object),
  ("f1", "int32"),
]))

#fig, ax = plt.subplots()
#ax.plot(n["f2"], n["f1"])

#plt.show()


import pmdarima as pm
from pmdarima.model_selection import train_test_split

# Load/split your data
y = n["f1"]
#train, test = train_test_split(y, train_size=20)

# Fit your model
model = pm.auto_arima(y, seasonal=True, m=1)

# make your forecasts
forecasts = model.predict(y.shape[0])  # predict N steps into the future

# Visualize the forecasts (blue=train, green=forecasts)
x = np.arange(y.shape[0])
plt.plot(x, y, c='green')
plt.plot(np.arange(2*y.shape[0])[y.shape[0]:], forecasts, c='blue')
plt.show()