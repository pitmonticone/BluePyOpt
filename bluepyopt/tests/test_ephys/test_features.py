"""Tests for ephys.efeatures"""

import os
from os.path import join as joinp

import pytest
import numpy

from bluepyopt.ephys import efeatures
from bluepyopt.ephys.responses import TimeVoltageResponse
from bluepyopt.ephys.serializer import instantiator


@pytest.mark.unit
def test_EFeature():
    """ephys.efeatures: Testing EFeature creation"""
    efeature = efeatures.EFeature('name')
    assert efeature.name == 'name'


@pytest.mark.unit
def test_eFELFeature():
    """ephys.efeatures: Testing eFELFeature creation"""
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature',
                                     efel_feature_name='voltage_base',
                                     recording_names=recording_names,
                                     stim_start=700,
                                     stim_end=2700,
                                     exp_mean=1,
                                     exp_std=1)

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    ret = efeature.calculate_feature(responses, raise_warnings=True)
    numpy.testing.assert_almost_equal(ret, -72.05761247316858)

    score = efeature.calculate_score(responses)
    numpy.testing.assert_almost_equal(score, 73.05761247316858)

    assert efeature.name == 'test_eFELFeature'
    assert 'voltage_base' in str(efeature)


@pytest.mark.unit
def test_eFELFeature_max_score():
    """ephys.efeatures: Testing eFELFeature max_score option"""

    recording_names = {'': 'square_pulse_step1.soma.v'}

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    efeature_normal = efeatures.eFELFeature(name='test_eFELFeature',
                                            efel_feature_name='AP_amplitude',
                                            recording_names=recording_names,
                                            stim_start=600,
                                            stim_end=700,
                                            exp_mean=1,
                                            exp_std=1)
    score_normal = efeature_normal.calculate_score(responses)
    numpy.testing.assert_almost_equal(score_normal, 250)

    efeature_150 = efeatures.eFELFeature(name='test_eFELFeature',
                                         efel_feature_name='AP_amplitude',
                                         recording_names=recording_names,
                                         stim_start=600,
                                         stim_end=700,
                                         exp_mean=1,
                                         exp_std=1,
                                         max_score=150)

    score_150 = efeature_150.calculate_score(responses)
    numpy.testing.assert_almost_equal(score_150, 150)


@pytest.mark.unit
def test_eFELFeature_force_max_score():
    """ephys.efeatures: Testing eFELFeature force_max_score option"""

    recording_names = {'': 'square_pulse_step1.soma.v'}

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    efeature_normal = efeatures.eFELFeature(name='test_eFELFeature',
                                            efel_feature_name='voltage_base',
                                            recording_names=recording_names,
                                            stim_start=700,
                                            stim_end=2700,
                                            exp_mean=1,
                                            exp_std=.001)
    score_normal = efeature_normal.calculate_score(responses)
    assert score_normal > 250

    efeature_force = efeatures.eFELFeature(name='test_eFELFeature',
                                           efel_feature_name='voltage_base',
                                           recording_names=recording_names,
                                           stim_start=700,
                                           stim_end=2700,
                                           exp_mean=1,
                                           exp_std=.001,
                                           force_max_score=True)

    score_force = efeature_force.calculate_score(responses)
    numpy.testing.assert_almost_equal(score_force, 250)


@pytest.mark.unit
def test_eFELFeature_double_settings():
    """ephys.efeatures: Testing eFELFeature double_settings"""
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature',
                                     efel_feature_name='voltage_base',
                                     recording_names=recording_names,
                                     stim_start=700,
                                     stim_end=2700,
                                     exp_mean=1,
                                     exp_std=1)
    efeature_ds = efeatures.eFELFeature(
        name='test_eFELFeature_other_perc',
        efel_feature_name='voltage_base',
        recording_names=recording_names,
        stim_start=700,
        stim_end=2700,
        exp_mean=1,
        exp_std=1,
        double_settings={
            'voltage_base_start_perc': 0.01})

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    vb_other_perc = efeature_ds.calculate_feature(
        responses,
        raise_warnings=True)
    vb = efeature.calculate_feature(responses, raise_warnings=True)

    assert vb_other_perc != vb


@pytest.mark.unit
def test_eFELFeature_int_settings():
    """ephys.efeatures: Testing eFELFeature int_settings"""
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature',
                                     efel_feature_name='Spikecount',
                                     recording_names=recording_names,
                                     stim_start=1200,
                                     stim_end=2000,
                                     exp_mean=1,
                                     exp_std=1)
    efeature_strict = efeatures.eFELFeature(
        name='test_eFELFeature_strict',
        efel_feature_name='Spikecount',
        recording_names=recording_names,
        stim_start=1200,
        stim_end=2000,
        exp_mean=1,
        exp_std=1,
        int_settings={
            'strict_stiminterval': True})

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    spikecount = efeature.calculate_feature(responses)
    spikecount_strict = efeature_strict.calculate_feature(responses)

    assert spikecount_strict != spikecount


@pytest.mark.unit
def test_eFELFeature_string_settings():
    """ephys.efeatures: Testing eFELFeature string_settings"""
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature_vb_default',
                                     efel_feature_name='voltage_base',
                                     recording_names=recording_names,
                                     stim_start=700,
                                     stim_end=2700)
    efeature_median = efeatures.eFELFeature(
        name='test_eFELFeature_vb_median',
        efel_feature_name='voltage_base',
        recording_names=recording_names,
        stim_start=700,
        stim_end=2700,
        string_settings={
            'voltage_base_mode': "median"})

    response = TimeVoltageResponse('mock_response')
    testdata_dir = joinp(
        os.path.dirname(
            os.path.abspath(__file__)),
        'testdata')
    response.read_csv(joinp(testdata_dir, 'TimeVoltageResponse.csv'))
    responses = {'square_pulse_step1.soma.v': response, }

    vb_median = efeature_median.calculate_feature(
        responses,
        raise_warnings=True)
    vb_default = efeature.calculate_feature(responses, raise_warnings=True)

    assert vb_median != vb_default


@pytest.mark.unit
def test_eFELFeature_serialize():
    """ephys.efeatures: Testing eFELFeature serialization"""
    recording_names = {'': 'square_pulse_step1.soma.v'}
    efeature = efeatures.eFELFeature(name='test_eFELFeature',
                                     efel_feature_name='voltage_base',
                                     recording_names=recording_names,
                                     stim_start=700,
                                     stim_end=2700,
                                     exp_mean=1,
                                     exp_std=1)
    serialized = efeature.to_dict()
    deserialized = instantiator(serialized)
    assert isinstance(deserialized, efeatures.eFELFeature)
    assert deserialized.stim_start == 700
    assert deserialized.recording_names == recording_names


@pytest.mark.unit
def test_extraFELFeature():
    """ephys.efeatures: Testing extraFELFeature calculation"""
    import pandas as pd

    somatic_recording_name = 'soma_response'
    recording_names = {'': 'lfp_response'}
    channel_ids = 0
    extrafel_feature_name = 'halfwidth'
    name = 'test_extraFELFeature'
    stim_start = 400
    stim_end = 1750
    fs = 10
    ms_cut = [10, 25]

    # load responses from file
    testdata_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'testdata'
    )
    resp_fname = os.path.join(testdata_dir, 'lfpy_response_with_soma.pkl')
    responses_lst = pd.read_pickle(resp_fname)
    responses = {
        somatic_recording_name: responses_lst[0][1],
        recording_names['']: responses_lst[0][0],
    }

    # compute for all electrodes
    efeature = efeatures.extraFELFeature(
        name=name,
        extrafel_feature_name=extrafel_feature_name,
        somatic_recording_name=somatic_recording_name,
        recording_names=recording_names,
        channel_ids=None,
        exp_mean=0.001,
        exp_std=0.001,
        stim_start=stim_start,
        stim_end=stim_end,
        fs=fs,
        ms_cut=ms_cut
    )

    ret = efeature.calculate_feature(responses, raise_warnings=True)
    assert len(ret) == 209

    # compute for 1 electrode
    efeature = efeatures.extraFELFeature(
        name=name,
        extrafel_feature_name=extrafel_feature_name,
        somatic_recording_name=somatic_recording_name,
        recording_names=recording_names,
        channel_ids=channel_ids,
        exp_mean=0.001,
        exp_std=0.001,
        stim_start=stim_start,
        stim_end=stim_end,
        fs=fs,
        ms_cut=ms_cut
    )

    ret = efeature.calculate_feature(responses, raise_warnings=True)
    numpy.testing.assert_almost_equal(ret, 0.0015)

    score = efeature.calculate_score(responses)
    numpy.testing.assert_almost_equal(score, 0.5)

    assert efeature.name == name
    assert extrafel_feature_name in str(efeature)
