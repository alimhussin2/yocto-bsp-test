#!/usr/bin/python3

from pylab import *
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
import peakutils
import subprocess

def record_audio_wave(audio_file):
    subprocess.run(["arecord", "-f", "cd", "-t", "wav", "--duration=10", audio_file])

def process_wav(audio_file):
    fs, snd = wavfile.read(audio_file)
    snd = snd / (2.**15) # sound value map to integer value with range -2^15 to (2^15)^-1
    s1 = snd[:,0] # use one channel
    # fft
    n = len(s1)
    p = fft(s1) # create fourier transform
    nUnique = int(ceil((n+1)/2.0))
    p = p[0: nUnique]
    p = abs(p)
    p = p / float(n) # scale by the number of points so that the magnitude does not depend
                 # on the length of signal 
    p = p**2 # square it to get power

    if n % 2 > 0: 
        p[1:len(p)] = p[1:len(p)] * 2
    else:
        p[1:len(p) - 1] = p[1:len(p) -1] * 2

    freqDomain = arange(0, nUnique, 1.0) * (fs / n)

    # find peak from fft
    peak_fft = peakutils.indexes(p, thres=0.1, min_dist=5)
    fig, ax = plt.subplots()
    for m in peak_fft:
        ax.scatter(freqDomain[m], 10*log10(p[m]), s=40, marker='s', color='red', label='peak')
        print('freq=%fHz, peak=%fdB' % (freqDomain[m], 10*log10(p[m])))
        f_signal = freqDomain[m]
        p_signal = 10*log10(p[m])
    sig_points = { "freq": f_signal, 
                   "power": p_signal }
    plt.plot(freqDomain, 10*log10(p))
    xlabel('Frequency (Hz)')
    ylabel('Power (dB)')
    plt.xlim(0.0,2000.0)
    plt.show()
    return sig_points


# test criteria
# if we found signal with freq ~ 750hz to 850hz then test pass
def detect_signal(f_low, f_high, power, f_signal, p_signal):
    if f_signal > f_low and f_signal < f_high:
        print("we found the signal with %.2fHz" % f_signal)
        if p_signal > power:
            print("This is signal that we found with %.2fdB" % p_signal)
    else:
        print("we not found the signal")

output_signal = {}
audio_file = 'record_sine_wave_800hz.wav'
#record_audio_wave(audio_file)
output_signal = process_wav(audio_file)
print(output_signal)
detect_signal(750.0, 850.0, -20.0, output_signal['freq'], output_signal['power'])



