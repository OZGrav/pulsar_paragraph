import pytest

from pulsar_paragraph.pulsar_paragraph import shklovski_pdot_correction

def test_shklovski_pdot_correction():
    pdot = 5.729214736380701e-20
    p = 0.0057574519367126365
    dist = 0.15679
    vtrans = 104.74457137561224
    pdot_corrected = shklovski_pdot_correction(pdot, p, dist, vtrans)
    assert pdot_corrected == pytest.approx(1.34e-20, rel=1e-2)