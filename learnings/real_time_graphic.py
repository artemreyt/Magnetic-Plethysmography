import numpy as np
import matplotlib.pyplot as plt

plt.axis([0, 10, 0, 1])

for i in range(10):
    y = np.random.random()
    plt.scatter(i, y)
    print(i)
    plt.axis([0, 10 + i, 0, 1])
    plt.pause(0.5)

plt.show()