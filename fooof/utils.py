"""Util functions for FOOOF."""

import numpy as np

###################################################################################################
###################################################################################################

def group_three(vec):
    """Takes array of inputs, groups by three.

	Parameters
	----------
	vec : 1d array
		Array of items to sort by 3 - must be divisible by three.

	Returns
	-------
	list of list
        List of lists, each with three items.
    """

    if len(vec) % 3 != 0:
        raise ValueError('Wrong size array to group by three.')

    return [list(vec[i:i+3]) for i in range(0, len(vec), 3)]


def trim_psd(freqs, psd, f_range, ignore_range=None):
    """Extract frequency range of interest from PSD data.

    Parameters
    ----------
    freqs : 1d array
        Frequency values for the PSD.
    psd : 1d array
        Power spectral density values.
    f_range : list of [float, float]
        Frequency range to restrict to.
    ignore_range : list of lists of [float, float], optional
        Inclusive range(s) of input (frequencies and corresponding PSD values) to exclude from fitting.

    Returns
    -------
    freqs_ext : 1d array
        Extracted power spectral density values.
    psd_ext : 1d array
        Extracted frequency values for the PSD.

    Notes
    -----
    This function extracts frequency ranges >= f_low and <= f_high.
        - It does not round to below or above f_low and f_high, respectively.
    It optionally excludes ranges within f_low and f_high to ignore during fitting
    """

    # Create mask to index only requested frequency range(s)
    f_mask = np.zeros_like(freqs)
    f_mask[np.logical_and(freqs >= f_range[0], freqs <= f_range[1])] = 1

    # If specified, ignore sub-range(s)
    if ignore_range != None:
        for ignore in ignore_range:
            f_mask[np.logical_and(freqs >= ignore[0], freqs <= ignore[1])] = 0
    
    # Restrict freqs & psd values to the specified range(s)
    freqs_ext = freqs[f_mask == 1]
    psd_ext = psd[f_mask == 1]

    return freqs_ext, psd_ext
