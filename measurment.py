import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from bitstring import BitArray
import serial
import os
import time
import numpy as np
import pylab
from scipy import fft, ifft
from scipy.optimize import curve_fit
from Pulse import get_fourier_result, max_point, beauty_picture
from peakdetect import _datacheck_peakdetect, _peakdetect_parabole_fitter, peakdetect, peakdetect_fft, peakdetect_parabole, peakdetect_sine, peakdetect_zero_crossing, _smooth, zero_crossings, _test_zero, _test,  _test_graph
from DigitalFilter import processing
import time


def calibration(port,speed):
    run(port, speed, "calibration", message=b'\xFF', saving=False, uGraph=False, iGraph=True)



def saveData(dirName, num, port1, port2):
    print("port1 = ", port1)
    print("port2 = ", port2)
    count = 0


    for i in range(len(port2)):
        fileName = dirName + "/%s.txt" % num
        with open(fileName, "a") as file:
            file.write(str(str(port2[i])))
            file.write("\n")
            count = count+1
    print('количество', count)



def parse_input_buffer(buf):
    null_bit = ord((buf[0])) & 1
    first_bit = (ord((buf[0])) & (1 << 1)) >> 1
    second_bit = (ord((buf[0])) & (1 << 2)) >> 2
    third_bit = (ord((buf[0])) & (1 << 3)) >> 3
    buf_int = []
    buf_int.append((ord((buf[1])) & 127) | (third_bit << 7))
    buf_int.append((ord((buf[2])) & 127) | (second_bit << 7))
    buf_int.append((ord((buf[3])) & 127) | (first_bit << 7))
    buf_int.append((ord((buf[4])) & 127) | (null_bit << 7))
    ch1 = (buf_int[0] << 24) | (buf_int[1] << 16) | (buf_int[2] << 8) | buf_int[3]
    if ch1 > 2**31:
        ch1 = ch1-2**32

    print("bulbul" + str(ch1 - 2**31))
   # ch1 = 0
    #k = 3
    #for num in buf:
     #   ch1 += num << k*8
      #  k = k-1
    return ch1


def read_one_byte(port):
    while port.in_waiting == 0:
        pass
    bt = port.read(1)
    return bt


def run(port, speed, duration, dirName, num=1, message=b'\01', saving=True, uGraph=True, iGraph=False):
    ser = serial.Serial(port=port,
                        baudrate=speed,
                        # stopBits=selectedStopBits
                        )  # open serial port

    print(ser.getSettingsDict())
    ser.isOpen()

    ser.write(message)
    data = ""

    full_data = []
    start = False
    endMeasurement = False

    while not start:
        one_byte = read_one_byte(ser)
        if one_byte == b'\x0f':
            start = True
            print("Started")
    print("Out of loop")

    begin_time = time.time()
    while not endMeasurement:
        data = []
        one_byte = read_one_byte(ser)
        if one_byte == b'\x07':
            print("Ended")
            break
        print("Not end")
        data.append(one_byte)
        while len(data) != 10:
            one_byte = read_one_byte(ser)
            data.append(one_byte)
        print(data)
        if time.time() - begin_time >= duration:
            endMeasurement = True
        else:
            full_data.append(data)


    ser.close()
    port1 = []
    port2 = []

    for i in range(len(full_data)):
        data1 = full_data[i]
        half1 = data1[:6]
        half2 = data1[5:]

        port2.append(parse_input_buffer(half2))
        port1.append(parse_input_buffer(half1))
        print(port1[i])
        print(port2[i])





    if saving:
        try:
            os.mkdir(dirName)
        except:
            pass
        saveData(dirName, num, port1, port2)

    # #if uGraph:
    # plt.figure(1)
    # plt.plot(range(len(port1)), port1)

    #if iGraph:
    plt.figure(1)
    plt.plot(range(len(port2)), port2)

    period = 1 / 488
    pulse_freq = 0.0
    new_spectra, freqs = get_fourier_result(port2, period)
    y_max, pulse_freq = max_point(new_spectra, freqs)
    #pulse_freq = f_of_max(new_spectra, freqs, y_max)
    beauty_spectra, beauty_freqs = beauty_picture(freqs, new_spectra)
    print(new_spectra)
    print(freqs)
    print('Максимальная точка = ', y_max)
    print('freq = ', pulse_freq)
    print('ЧСС = ', round(60 * pulse_freq, 2))

    U = []
    U = processing(port2)


    plt.figure(2)
    plt.plot(freqs, new_spectra)

    plt.figure(3)
    plt.plot(beauty_freqs, beauty_spectra)

    plt.figure(4)
    plt.plot(U)


    # plt.show()
    plt.savefig('graph.png')





