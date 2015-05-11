__author__ = 'kyle'

import numpy as np
from scipy.io import wavfile
from scipy import signal
import matplotlib.pyplot as plt


def stft(x, fftlen, hop):
    """
    :param x: Time domain signal to be transformed.
    :param fftlen: Length of a single fft in samples.
    :param hop: Number of samples to move forward before starting next window
    :return: Returns a 2D array. First index addresses time position of spectrum,
    second index refers to individual frequency spectra.
    """
    w = np.hanning(fftlen)
    return np.array([np.fft.rfft(w * x[i:i + fftlen]) for i in range(0, len(x) - fftlen, hop)])


def istft(spec, hop):
    """
    :param spec: The result of an stft, spectra at different times
    :param hop: number of smaples to move forward between windows
    :return: time domain signal which is related to the original by a constant coefficient.

    fftlen inferred from shape of input vector.
    """
    fftlen = 2 * (spec.shape[1] - 1)
    xs = np.empty((spec.shape[0], fftlen))
    w = np.hanning(fftlen)

    out = np.empty(spec.shape[0] * hop + fftlen,
                   dtype=complex)  # Need a quick calc to find the length of the output array
    phase = np.zeros(spec.shape[1])
    adj = np.zeros(spec.shape[1], dtype=complex)

    for t in range(spec.shape[0]):
        if t > 0:
            phase += np.angle(spec[t]) - np.angle(spec[t - 1])
            phase %= 2 * np.pi
            adj.real, adj.imag = np.cos(phase), np.sin(phase)

        # xs[t] = np.fft.ifft(Xs[t])
        xs[t] = np.fft.irfft(np.abs(spec[t]) * adj)
        out[t * hop: t * hop + fftlen] += xs[t] * w

    return out


def mystretch(x, s, fftsize):
    """
    :param x: The sound array read in from a wave.
    :param s: Factor to speed up the sound
    :param fftsize: window size
    :return: time domain signal stretched by fac.
    """
    hop = fftsize / 4
    w = np.hanning(fftsize)
    phi = np.zeros(fftsize / 2 + 1)
    #phi = np.zeros(fftsize) #This one for fft, other one for rfft
    out = np.zeros(len(x) / s + fftsize)

    for t in np.arange(0, len(x) - (fftsize + hop), hop * s):
        seg1 = x[t : t + fftsize]
        seg2 = x[t + hop : t + hop + fftsize]

        spec1 = np.fft.rfft(seg1 * w)
        spec2 = np.fft.rfft(seg2 * w)

        phi += np.angle(spec2 / spec1) % (2 * np.pi)
        phi %= 2*np.pi

        seg2rp = np.fft.irfft(np.abs(spec2) * np.exp(1j * phi))

        t2 = int(t / s)
        out[t2 : t2 + fftsize] += w * seg2rp

    out = ((2**(16-4)) * out / out.max())
    return out.astype('int16')


def stretch(snd_array, factor, window_size, h):
   """ Stretches/shortens a sound, by some factor. """
   phase  = np.zeros(window_size)
   hanning_window = np.hanning(window_size)
   result = np.zeros( len(snd_array) /factor + window_size)
   for i in np.arange(0, len(snd_array)-(window_size+h), h*factor):
       # two potentially overlapping subarrays
       a1 = snd_array[i: i + window_size]
       a2 = snd_array[i + h: i + window_size + h]
       # the spectra of these arrays
       s1 =  np.fft.fft(hanning_window * a1)
       s2 =  np.fft.fft(hanning_window * a2)
       #  rephase all frequencies
       phase = (phase + np.angle(s2/s1)) % 2*np.pi
       a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
       i2 = int(i/factor)
       result[i2 : i2 + window_size] += hanning_window*a2_rephased
   result = ((2**(16-4)) * result/result.max()) # normalize (16bit)
   return result.astype('int16')


#if __name__ == '__main__':
#    fps, bowl_sound = wavfile.read("bowl.wav")
#    #ts = np.linspace(0, 100, 2 ** 18, dtype = 'int16')
#    #sq = signal.square(ts)
#    fftlen = 2**12
#    s = 0.25
#    data = mystretch(bowl_sound, s, fftlen)
#    data *= 4
#    plt.plot(bowl_sound)
#    plt.plot(data)
#    plt.show()
#    wavfile.write("bowl_stretched.wav", fps, data)