import numpy as np
import scipy
import matplotlib.pyplot as plt


def stft(x, fftsize=1024, overlap=4):
    """fftsize is in samples
    """

    hop = fftsize / overlap
    w = scipy.hanning(fftsize + 1)[:-1]  # better reconstruction with this trick +1)[:-1]
    return np.array([np.fft.rfft(w * x[i:i + fftsize]) for i in range(0, len(x) - fftsize, hop)])


def istft(X, overlap=4):
    fftsize = (X.shape[1] - 1) * 2
    hop = fftsize / overlap
    w = scipy.hanning(fftsize + 1)[:-1]
    x = scipy.zeros((X.shape[0] + overlap) * hop)
    wsum = scipy.zeros((X.shape[0] + overlap) * hop)
    for n, i in enumerate(range(0, len(x) - fftsize, hop)):
        x[i:i + fftsize] += scipy.real(np.fft.irfft(X[n])) * w  # overlap-add
        wsum[i:i + fftsize] += w ** 2.
    pos = wsum != 0
    x[pos] /= wsum[pos]
    return x