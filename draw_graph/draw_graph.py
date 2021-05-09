import matplotlib.pyplot as plt
import numpy as np

filename = '1.txt'
count = 0
port1 = []
port2 = []
with open(filename) as f:
    duration = int(f.readline())
    for line in f:
        port1_val, port2_val = map(int, line.split())
        port1.append(port1_val)
        port2.append(port2_val)
        count += 1

x = np.linspace(0., duration, count)
line_port1, = plt.plot(x, port1, label='port 1')
#line_port2, = plt.plot(x, port2, label='port 2')
plt.legend()
plt.ylabel('U, V')
plt.xlabel('Time, s')
plt.show()