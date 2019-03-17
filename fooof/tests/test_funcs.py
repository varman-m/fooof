"""Test functions for ..."""

from py.test import raises

import numpy as np

from fooof.utils import compare_info
from fooof.group import FOOOFGroup
from fooof.synth import gen_group_power_spectra

from fooof.funcs import *
from fooof.tests.utils import default_group_params

###################################################################################################
###################################################################################################

def test_combine_fooofs(tfm, tfg):

    tfm2 = tfm.copy(); tfm3 = tfm.copy()
    tfg2 = tfg.copy(); tfg3 = tfg.copy()

    # Check combining 2 FOOOFs
    nfg1 = combine_fooofs([tfm, tfm2])
    assert nfg1
    assert len(nfg1) == 2
    assert compare_info([nfg1, tfm], 'settings')
    assert nfg1.group_results[0] == tfm.get_results()
    assert nfg1.group_results[-1] == tfm2.get_results()

    # Check combining 3 FOOOFs
    nfg2 = combine_fooofs([tfm, tfm2, tfm3])
    assert nfg2
    assert len(nfg2) == 3
    assert compare_info([nfg2, tfm], 'settings')
    assert nfg2.group_results[0] == tfm.get_results()
    assert nfg2.group_results[-1] == tfm3.get_results()

    # Check combining 2 FOOOFGroups
    nfg3 = combine_fooofs([tfg, tfg2])
    assert nfg3
    assert len(nfg3) == len(tfg) + len(tfg2)
    assert compare_info([nfg3, tfg, tfg2], 'settings')
    assert nfg3.group_results[0] == tfg.group_results[0]
    assert nfg3.group_results[-1] == tfg2.group_results[-1]

    # Check combining 3 FOOOFGroups
    nfg4 = combine_fooofs([tfg, tfg2, tfg3])
    assert nfg4
    assert len(nfg4) == len(tfg) + len(tfg2) + len(tfg3)
    assert compare_info([nfg4, tfg, tfg2, tfg3], 'settings')
    assert nfg4.group_results[0] == tfg.group_results[0]
    assert nfg4.group_results[-1] == tfg3.group_results[-1]

    # Check combining a mixture of FOOOF & FOOOFGroup
    nfg5 = combine_fooofs([tfg, tfm, tfg2, tfm2])
    assert nfg5
    assert len(nfg5) == len(tfg) + 1 + len(tfg2) + 1
    assert compare_info([nfg5, tfg, tfm, tfg2, tfm2], 'settings')
    assert nfg5.group_results[0] == tfg.group_results[0]
    assert nfg5.group_results[-1] == tfm2.get_results()

    # Check combining objects with no data
    tfm2._reset_data_results(False, True, True)
    tfg2._reset_data_results(False, True, True, True)
    nfg6 = combine_fooofs([tfm2, tfg2])
    assert len(nfg6) == 1 + len(tfg2)
    assert nfg6.power_spectra == None

def test_combine_errors(tfm, tfg):

    # Incompatible settings
    for f_obj in [tfm, tfg]:
        f_obj2 = f_obj.copy()
        f_obj2.peak_width_limits = [2, 4]
        f_obj2._reset_internal_settings()

        with raises(ValueError):
            combine_fooofs([f_obj, f_obj2])

    # Incompatible data information
    for f_obj in [tfm, tfg]:
        f_obj2 = f_obj.copy()
        f_obj2.freq_range= [5, 30]

        with raises(ValueError):
            combine_fooofs([f_obj, f_obj2])

def test_fit_fooof_group_3d(tfg):

    n_spectra = 2
    xs, ys, _ = gen_group_power_spectra(n_spectra, *default_group_params())
    ys = np.stack([ys, ys], axis=0)

    tfg = FOOOFGroup()
    fgs = fit_fooof_group_3d(tfg, xs, ys)

    assert len(fgs) == 2
    for fg in fgs:
        assert fg
