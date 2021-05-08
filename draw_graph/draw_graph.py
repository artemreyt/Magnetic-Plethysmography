import matplotlib.pyplot as plt

filename = '1.txt'
count = 0
y = []
with open(filename) as f:
    for str_value in f:
        y.append(int(str_value))
        count += 1
plt.plot(range(count), y)
plt.ylabel('U, V')
plt.xlabel('Time, s')
plt.show()