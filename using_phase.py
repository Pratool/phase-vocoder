import numpy as np
import matplotlib.pyplot as plt
from stft import stft

if __name__ == "__main__":
    fr = 44100  # framerate
    time = np.arange(0, 5, 1.0/fr)

    # Generate 100 Hz sin wave
    sig = np.sin(100*time)
    plt.plot(time, sig)
    plt.axis([0, 5, -2, 2])
    plt.show()

    # Generate windows
    windows = stft(sig)
    print len(windows)
    plt.plot(np.abs(windows[8]))
    plt.plot(np.abs(windows[9]))
    plt.show()

