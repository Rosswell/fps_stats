import os
import csv
from datetime import datetime


cwd = os.getcwd()

stats_files = [f for f in os.listdir(cwd) if os.path.isfile(os.path.join(cwd, f)) and f.endswith('.csv')]

for file in stats_files:
    with open(file, 'r') as f:
        date = datetime.strptime(file.split(' ')[-2], '%Y.%m.%d-%H.%M.%S')
        data = {
            'Date': date,
            'TTK': [],
            'Shots': [],
            'Accuracy': [],
            'Efficiency': [],
            'Score': 0,
            'Map': ''
        }
        reader = csv.reader(f)
        for row in reader:
            if len(row) < 1:
                continue
            if row[0] in [str(x) for x in range(100)]:
                # individual kill stats
                data['TTK'].append(float(row[4][:-1]))
                data['Shots'].append(int(row[5]))
                data['Accuracy'].append(float(row[7]))
                data['Efficiency'].append(float(row[10]))
            if row[0] == 'Score:':
                data['Score'] = float(row[1])
                if float(row[1]) == 0.0:
                    break
            if row[0] == 'Scenario:':
                data['Map'] = row[1]
                print(data)
                continue

            
