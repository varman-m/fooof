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

    # If specified, ignore sub-range(s) by replacing values with linear curve defined by range's endpoints
    if ignore_range != None:
        
        freq_res = freqs[1] - freqs[0]
        for ignore in ignore_range:
            l_ind = int(np.floor(ignore[0] / freq_res))
            r_ind = int(np.ceil(ignore[1] / freq_res))
            y_0 = psd[l_ind]
            y_1 = psd[r_ind]
            x_0 = freqs[l_ind]
            x_1 = freqs[r_ind]
            slope = (y_0 - y_1)/(x_0 - x_1)

            # List of indices of PSD replacement between left and right points of current ignore_range
            replace_range = np.arange(l_ind, r_ind+1, 1)

            # Replace the PSD values by line defined by slope & y-int
            for index in replace_range:
                psd[index] = (slope * index) + y_0
            
    # Restrict freqs & psd values to the specified range(s)
    freqs_ext = freqs[f_mask == 1]
    psd_ext = psd[f_mask == 1]

    return freqs_ext, psd_ext