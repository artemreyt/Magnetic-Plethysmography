
import numpy as np


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
    for i in range(6, 35):
        if y_max == new_spectra[i]:
            pulse_freq = freqs[i]
    return pulse_freq

def beauty_picture(freqs, spectra):
    beauty_freqs = []
    beauty_spectra = []
    for i in range(0, 35):
        beauty_freqs.append(freqs[i])
        beauty_spectra.append(spectra[i])
    return beauty_spectra, beauty_freqs