#!/usr/bin/env python
"""  """

from py.test import raises
import numpy as np

from fooof.utils import group_three, trim_psd #overlap

##
##

# def test_overlap():

# 	lst_1 = [10, 12]
# 	lst_2 = [8, 13]
# 	lst_3 = [9, 14]

# 	assert overlap(lst_1, lst_2)
# 	assert not overlap(lst_2, lst_1)
# 	assert not overlap(lst_2, lst_3)

def test_group_three():

	dat = [0, 1, 2, 3, 4, 5]
	assert group_three(dat) == [[0, 1, 2], [3, 4, 5]]

	with raises(ValueError):
		group_three([0, 1, 2, 3])

def test_trim_psd():
	# NOTE: fix test when desired behaviour is specified and updated.

	f_in = np.array([0., 1., 2., 3., 4., 5.])
	p_in = np.array([1., 2., 3., 4., 5., 6.])

	f_out, p_out = trim_psd(f_in, p_in, [2., 4.])

	assert np.array_equal(f_out, np.array([2., 3., 4.]))
	assert np.array_equal(p_out, np.array([3., 4., 5.]))
    
# test trim_psd() with optional ignore_range parameter
def test_trim_psd_and_ignore():
    
    f_in = np.arange(1., 10, 1)
    p_in = np.arange(1., 10, 1)
    f_range = [1, 9]
    ign_range = [[3, 4], [5, 6]]
    
    f_out, p_out = trim_psd(f_in, p_in, f_range, ignore_range=ign_range)
    
    assert np.array_equal(f_out, np.array([1., 2., 7., 8., 9.]))
    assert np.array_equal(p_out, np.array([1., 2., 7., 8., 9.]))

