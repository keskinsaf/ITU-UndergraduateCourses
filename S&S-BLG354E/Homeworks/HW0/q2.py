import numpy as np
import matplotlib.pyplot as plt
import functools
import scipy.io.wavfile as siow

import q1

pi  = np.pi
sin = np.sin
cos = np.cos

rng = 30

time = np.arange(-rng*np.pi, rng * np.pi, 0.1)
f1 = q1.f

wav_writer = siow.write
wav_reader = siow.read

def all_true(seq):
    return functools.reduce( (lambda x,y: x == y and x == True), seq )

def f2(t):
    return t * 3 / 2 + pi / 4

def f3(t):
    return t/4

functions = [ f1, f2, f3, (lambda t: t* 3 * 4 / 24 + pi / 3), lambda t: t * 24 / 11 ]

if __name__ == "__main__":
    signals = [ sin(f(time)) for f in functions ]
    signals = signals + [ cos(f(time)) for f in functions ]
    result_signal = np.sum(signals, axis=0)
    name44 = "q2/44khz.wav"
    name22 = "q2/22khz.wav"
    name11 = "q2/11khz.wav"

    # wav_writer(name44, 44100, result_signal)
    # wav_writer(name22, 22050, result_signal)
    # wav_writer(name11, 11025, result_signal)
    # print("plotting initial signal")
    # plt.plot(time,result_signal)
    # plt.title("initial signal")
    # plt.show()
    
    print("Reading 44khz")
    rate,read44 = wav_reader(name44)

    # plt.plot(time, read44)
    # plt.show()
    
    print("Reading 22khz")
    rate,read22 = wav_reader(name22)

    # plt.plot(time, read22)
    # plt.show()

    print("Reading 11khz")
    rate,read11 = wav_reader(name11)

    # plt.plot(time, read11)
    # plt.show()

    print( all_true(read44 == read22) )
    print( all_true(read44 == read11) )
    print( all_true(read22 == read11) )