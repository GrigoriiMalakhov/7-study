import matplotlib.pyplot as plt
import numpy as np

#### LOAD_DATA ####
data = np.loadtxt("data.txt", dtype=int) * 3.3 / 256
settings = np.loadtxt("settings.txt", dtype=float)
time = np.linspace(0, settings[1]*len(data), len(data))
ch_time = time[np.argmax(data)]
dis_time = time[len(data)-1] - ch_time

#### GRID ####
fig, ax = plt.subplots()
ax.grid(which='major', color='grey', linestyle='-')
ax.grid(which='minor', linewidth=0.2, color='grey', linestyle='--')

#### AXES ####
max_data = np.max(data)
min_data = np.min(data)
ax.set(ylim=(min_data, max_data*1.1))
ax.set_xlabel(xlabel='Time, s')
ax.set_ylabel(ylabel='Voltage, V')
ax.set_title(label='The process of charging and discharging a capacitor in an RC-circuit')
xticks = []
tmp = 0
for i in range(20):
    xticks.append(tmp)
    tmp += 0.5
yticks = []
tmp = 0
for i in range(35):
    yticks.append(tmp)
    tmp += 0.1
ax.set_xticks(xticks, minor=True)
ax.set_yticks(yticks, minor=True)

#### DRAWING PLOT ####
ax.plot(time, data, linewidth=2, marker='o', markeredgewidth=0.2, markersize=7, markevery=30, label='V(t)')
ch_str = 'Time of charging: ' + str(ch_time)
dis_str = 'Time of discharging: ' + str(dis_time)
ax.text(x= 5.5, y= 2.5, s=ch_str)
ax.text(x= 5.5, y= 2.3, s=dis_str)
ax.legend()
fig.savefig('plot.svg')
plt.show()