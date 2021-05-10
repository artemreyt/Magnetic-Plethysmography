import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import os

def draw_ports(duration, port1=None, port2=None):
    assert port1 != None or port2 != None
    matplotlib.use('qt5agg')

    if port1:
        plt.plot(np.linspace(0., duration, len(port1)), port1, label='port 1')
    if port2:
        plt.plot(np.linspace(0., duration, len(port2)), port2, label='port 2')
    plt.legend()
    plt.ylabel('U, V')
    plt.xlabel('Time, s')
    plt.show()


def draw_ports_from_file(filename, draw_port1=True, draw_port2=True):
    port1 = [] if draw_port1 else None
    port2 = [] if draw_port2 else None

    with open(filename) as f:
        duration = int(f.readline())
        for line in f:
            port1_val, port2_val = map(int, line.split())
            if draw_port1:
                port1.append(port1_val)
            if draw_port2:
                port2.append(port2_val)
    draw_ports(duration, port1, port2)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <filename>')
        sys.exit(-1)
    filename = sys.argv[1]
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        print(f'{filename} not exist or not a file')
    # draw_portN = True, если печатать, False если не надо печатать
    draw_ports_from_file(filename, draw_port1=False, draw_port2=True)
