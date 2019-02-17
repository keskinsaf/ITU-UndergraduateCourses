import numpy as np
import scipy.io.wavfile as siow
from vispy import plot as vp

if __name__ == "__main__":
    wav_reader = siow.read

    f_name = "spec.wav"
    rate, data = wav_reader(f_name)

    fs = 1000.
    N = data.shape[0]
    t = np.arange(N) / float(fs)
    
    plot_data = np.array( (t, data))

    fig = vp.Fig(size=(800, 400), show=False)
    fig[0:2, 0].spectrogram(data, fs=fs, clim=(-100, -20))
    fig[2, 0].plot( plot_data.T, marker_size=0)
    fig.show(run=True)