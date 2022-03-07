#!/usr/bin/env python

"""filters.py: A robust Butterworth filter to clean bio-signals."""

__author__      = "Jes'us Fuentes"
__copyright__   = "Copyright 2021, LCSB"

from __future__ import division

import numpy as np
import scipy
import scipy.signal
import scipy.ndimage

def preFilter(lowcut=None, highcut=None, sampling_rate=125, normalize=False):
    # Checking Nyquist frequency
    if isinstance(highcut, int):
        if sampling_rate <= 2 * highcut:
            warn("Warning! -- Sampling frequency below Nyquist frequency")

    # Replace 0 by none
    if lowcut is not None and lowcut == 0:
        lowcut = None
    if highcut is not None and highcut == 0:
        highcut = None

    # Classification
    freqs = 0
    filter_type = ""
    if lowcut is not None and highcut is not None:
        if lowcut > highcut:
            filter_type = "bandstop"
        else:
            filter_type = "bandpass"
        freqs = [lowcut, highcut]

    elif lowcut is not None:
        freqs = [lowcut]
        filter_type = "highpass"

    elif highcut is not None:
        freqs = [highcut]
        filter_type = "lowpass"

    # Offset: fixing frequency to Nyquist frequency
    if normalize is True:
        freqs = np.array(freqs) / (sampling_rate / 2)

    return freqs, filter_type


"""
    Butterworth filter for ECG/PPG signals.
    ---------------------------------------
"""

def filterSig(signal, sampling_rate):
    # Apply high-pass, Butterworth filter to PPG/ECG signal
    freqs, filter_type = preFilter(lowcut=0.5, highcut=None, sampling_rate=sampling_rate)

    # Compute SOS
    order = 5
    sos = scipy.signal.butter(order, freqs, btype=filter_type, output="sos", fs=sampling_rate)
    filtered = scipy.signal.sosfiltfilt(sos, signal)

    # Apply filter to remove DC
    powerline = 50

    # Preparing all arrays
    if sampling_rate >= 100:
        b = np.ones(int(sampling_rate / powerline))
    else:
        b = np.ones(2)
    a = [len(b)]

    return scipy.signal.filtfilt(b, a, filtered, method="pad")
