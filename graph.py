import numpy as np
import matplotlib.pyplot as plt
from peakdetect import _datacheck_peakdetect, _peakdetect_parabole_fitter, peakdetect, peakdetect_fft, peakdetect_parabole, peakdetect_sine, peakdetect_zero_crossing, _smooth, zero_crossings, _test_zero, _test,  _test_graph
import pylab
import os
from scipy import signal as sp_sig
from scipy.stats import moment
# import pywt
from scipy.signal import butter, lfilter, lfilter_zi, welch
from scipy.signal import find_peaks_cwt
from scipy.signal import correlate
from scipy.signal import cwt
from scipy.interpolate import CubicSpline
import math
import csv
import time
#from math_utils import *


def get_fourier_result (signal, period):
    complex_four = np.fft.fft(signal)
    spectra = np.absolute(complex_four)
    freqs = []
    for i in range(0, int(len(signal) / 2)):
        freqs.append(1 / (period * len(signal)) * i)

    new_spectra = []
    for i in range(0, int(len(signal) / 2)):
        new_spectra.append(spectra[i])
    return new_spectra, freqs

def max_point (new_spectra, freqs):
    max_mas = []
    f_mas = []
    for i in range(4, 35):
        if (new_spectra[i] > new_spectra[i - 1]) and (new_spectra[i] > new_spectra[i + 1]):
            max_mas.append(new_spectra[i])
            f_mas.append(freqs[i])
    if len(max_mas) == 0:
        print('Сигнал такой себе')
    print ('aaa =', max_mas)
    y_max = max(max_mas)
    f_max = 0.0
    print(y_max)
    for num in range(0, len(max_mas)):
        if max_mas[num] == y_max:
            f_max = f_mas[num]
            print(f_max)
    return y_max, f_max

def f_of_max (new_spectra, freqs, y_max):
    pulse_freq = 0.0
    for i in range(0, len(freqs)):
        if y_max == new_spectra[i]:
            pulse_freq = freqs[i]
    return pulse_freq

def beauty_picture(freqs, spectra):
    beauty_freqs = []
    beauty_spectra = []
    for i in range(0, 50):
        beauty_freqs.append(freqs[i])
        beauty_spectra.append(spectra[i])
    return beauty_spectra, beauty_freqs



fileNamee = r"C:\Users\vika-\Magnetic-Plethysmography\perfect.txt"
signal = []
x = []
i = 0

# read file
with open(fileNamee, "r") as file:
    for line in file:
        line = line[7:]
        signal.append(float(line[:-1]))
        x.append(i)
        i = i + 1
max = []
min = []
max, min = peakdetect(signal, x, 750, 0.30)
xm = [p[0] for p in max]
ym = [p[1] for p in max]
xn = [p[0] for p in min]
yn = [p[1] for p in min]

plot = pylab.plot(x, signal)
# pylab.hold(True)
pylab.plot(xm, ym, 'r+')
pylab.plot(xn, yn, 'g+')
plt.plot(x, signal, color ='pink')
plt.show()

 #i = 10000

 #y *= -1






#period = 1/488
#new_spectra, freqs = get_fourier_result(signal, period)
#y_max, pulse_freq = max_point(new_spectra, freqs)
#pulse_freq = 0.0
#pulse_freq = f_of_max (new_spectra, freqs, y_max)
#beauty_spectra, beauty_freqs = beauty_picture(freqs, new_spectra)
#print(new_spectra)
#print(freqs)
#print('Максимальная точка = ', y_max)
#print('freq = ', pulse_freq)
#print('ЧСС = ', round(60*pulse_freq,2))

#plt.figure(1)
#plt.plot(range(len(signal)), signal)
#plt.xlabel('Time(s)')
#plt.ylabel('U(mV)')

#plt.figure(2)
#plt.plot(freqs, new_spectra)
#plt.xlabel('Frequency(Hz)')

#plt.figure(3)
#plt.plot(beauty_freqs, beauty_spectra)
#plt.xlabel('Frequency(Hz)')

