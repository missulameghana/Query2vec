import matplotlib.pyplot as plt
import csv

x = []
y = []

with open('example.csv','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(float(row[0]))
        y.append(float(row[1]))

plt.scatter(x,y)
plt.xlabel('average execution time in seconds')
plt.ylabel('cluster number')
plt.savefig('file.png')