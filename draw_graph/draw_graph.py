import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys
import os

import numpy.fft
from scipy import signal
import json

config_filename = "config.json"

def mean_absolute_error(raw, filtered):
    np_raw, np_filtered = np.array(raw), np.array(filtered)
    return np.sum(np.abs(np_raw - np_filtered))/ len(np_raw)

def highpass_filter_signal_port1(sig):
    fc = 10
    w = fc / (len(sig) / 2)
    b, a = signal.butter(5, w, btype='high')
    return signal.filtfilt(b, a, sig)

def lowpass_filter_signal_port1(sig):
    fc = 70
    w = fc / (len(sig) / 2)
    b, a = signal.butter(5, w, 'low')
    return signal.filtfilt(b, a, sig)


def highpass_filter_signal_port2(sig):
    fc = 10
    w = fc / (len(sig) / 2)
    b, a = signal.butter(5, w, btype='high')
    return signal.filtfilt(b, a, sig)

def lowpass_filter_signal_port2(sig):
    fc = 70
    w = fc / (len(sig) / 2)
    b, a = signal.butter(5, w, 'low')
    return signal.filtfilt(b, a, sig)

def calc_hc(peaks, time_seq):
    periods = []
    print("Periods:", end=" ")
    for i in range(len(peaks) - 1):
        period = time_seq[peaks[i + 1]] - time_seq[peaks[i]]
        periods.append(period)
        print(round(period, 3), end=" ")
    mid_period = sum(periods) / len(periods)
    print(f"\nMiddle period = { mid_period }")
    hc = 60 / mid_period
    print(f"ЧСС = {hc}")
    return hc

def draw_ports(duration, port1, port2, config=None):
    if config is None:
        config = PlotConfig()

    matplotlib.use('qt5agg')
    # fig = plt.figure()

    title = ""
    if any(config.port1):

        port1_filtered_highpass = highpass_filter_signal_port1(port1)
        port1_filtered_lowpass = lowpass_filter_signal_port1(port1_filtered_highpass)
        x = np.linspace(0., duration, len(port1))

        if config.port1["self"]:
            plt.plot(x, port1, label='port 1')
        if config.port1["lowpass"]:
            plt.plot(x, port1_filtered_lowpass, label='port 1 filtered')
        if config.port1["highpass"]:
            plt.plot(x, port1_filtered_highpass, label='port 1 filtered highpass')
        if config.port1["peaks"]:
            peaks, _ = signal.find_peaks(port1_filtered_highpass, height=max(port1_filtered_highpass)/2)
            plt.plot(x[peaks], port1_filtered_highpass[peaks], 'x', label='peaks port1_filtered_highpass')
            port1_heart_rate = len(peaks) * 60 / duration
            title += f'ЧСС1={port1_heart_rate} '

    if any(config.port2):

        port2_filtered_highpass = highpass_filter_signal_port2(port2)
        port2_filtered_lowpass = lowpass_filter_signal_port2(port2_filtered_highpass)
        x = np.linspace(0., duration, len(port2))

        # fig, axs = plt.subplots(2)
        if config.port2["self"]:
            plt.plot(x, port2, label='port 2')
        if config.port2["highpass"]:
            plt.plot(x, port2_filtered_highpass,
                label=f'port 2 filtered highpass, MAE = {mean_absolute_error(port2_filtered_lowpass, port2_filtered_highpass)}')
        if config.port2["lowpass"]:
            plt.plot(x, port2_filtered_lowpass, label='port 2 filtered lowpass')
        if config.port2["peaks"]:
            peaks, _ = signal.find_peaks(port2_filtered_lowpass, height=max(port2_filtered_lowpass) * 0.45)
            plt.plot(x[peaks], port2_filtered_lowpass[peaks], 'x', label='peaks port2_filtered_lowpass')
            title += f'ЧСС2={calc_hc(peaks, x)}'
        plt.title(title)

        freq = np.arange(0, 0.1, 1/488)
        # fft_port2_lowpass = np.absolute(numpy.fft.fft(port2_filtered_lowpass))[:len(freq)]
        # axs[1].plot(freq, fft_port2_lowpass)

    plt.legend()
    # plt.ylabel('U, V')
    plt.xlabel('Time, s')
    plt.show()


def draw_ports_from_file(filename, config_filename=None):
    config = PlotConfig(config_filename)

    port1 = []
    port2 = []

    with open(filename) as f:
        duration = int(f.readline())
        for line in f:
            port1_val, port2_val = map(int, line.split())
            port1.append(port1_val)
            port2.append(port2_val)
    draw_ports(duration, port1, port2, config)


def load_json_from_file(filename):
    with open(filename, "r") as f:
        json_dict = json.load(f)
    return json_dict


class PlotConfig:
    def __init__(self, config_filename=None):
        if config_filename:
            json_config = load_json_from_file(config_filename)
            for key, value in json_config.items():
                self.__dict__[key] = value
        else:
            for port in ["port1", "port2"]:
                self.__dict__[port] = {
                    "self": True,
                    "lowpass": True,
                    "highpass": True,
                    "peaks": True
                }


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(f'Usage: {sys.argv[0]} <filename>')
        sys.exit(-1)
    filename = sys.argv[1]
    if not (os.path.exists(filename) and os.path.isfile(filename)):
        print(f'{filename} not exist or not a file')
    draw_ports_from_file(filename, config_filename)
