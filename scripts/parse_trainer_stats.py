import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

import pandas as pd

cwd = os.path.join(os.getcwd(), '..')
stats_files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)) and f.endswith('.csv')]
columns = ['date', 'ttk', 'shots', 'accuracy', 'efficiency', 'score', 'map']
df = pd.DataFrame(columns=columns)


def add_to_df(dataframe, data):
    l = len(data['ttk'])
    # data['date'] = [data['date']] * l
    # data['score'] = [data['score']] * l
    # data['map'] = [data['map']] * l
    # for i in range(l):
    #     temp_data = {}
    #     for col in columns:
    #         temp_data[col] = data[col][i]
    #     dataframe = dataframe.append(temp_data, ignore_index=True)
    ttk = np.average(data['ttk'])
    shots = np.average(data['shots'])
    acc = np.average(data['accuracy'])
    eff = np.average(data['efficiency'])

    return dataframe.append({k: v for k, v in zip(columns, [data['date'], ttk, shots, acc, eff, data['score'], data['map']])}, ignore_index=True)


for file in stats_files:
    with open(os.path.join('..', file), 'r') as f:
        date = datetime.strptime(file.split(' ')[-2], '%Y.%m.%d-%H.%M.%S')
        data = {
            'date': date,
            'ttk': [],
            'shots': [],
            'accuracy': [],
            'efficiency': [],
            'score': 0,
            'map': ''
        }
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 1:
                continue
            if row[0] in [str(x) for x in range(100)]:
                # individual kill stats
                data['ttk'].append(float(row[4][:-1]))
                data['shots'].append(int(row[5]))
                data['accuracy'].append(float(row[7]))
                data['efficiency'].append(float(row[10]))
            if row[0] == 'Score:':
                data['score'] = float(row[1])
                if float(row[1]) == 0.0:
                    break
            if row[0] == 'Scenario:':
                data['map'] = row[1]
                df = add_to_df(df, data)
                continue

df = df.dropna()
df = df.set_index('date')
df = df.sort_index()
df = df.reset_index()

df[['accuracy']][df['map'] == 'Ascended Tracking v3'].plot()
plt.show()
