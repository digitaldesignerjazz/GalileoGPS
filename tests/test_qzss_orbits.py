from galileogps.qzss_orbits import QZS4, QZS5, get_slot


def test_qzs4_operational_qzo():
    assert QZS4.status == "operational"
    assert QZS4.orbit_class == "QZO"
    assert QZS4.prn_pnt == 195
    assert QZS4.lambda_east_deg == 137.5
    assert QZS4.raan_deg == 347.0
    assert abs(QZS4.perigee_alt_km - 32624.5) < 2.0
    assert abs(QZS4.apogee_alt_km - 38949.2) < 2.0


def test_qzs5_lost_design_slot():
    slot = get_slot("QZS-5")
    assert slot is QZS5
    assert QZS5.status == "lost"
    assert QZS5.orbit_class == "QZO"
    assert QZS5.prn_pnt is None
    assert QZS5.lambda_east_deg == 139.0
    assert QZS5.raan_deg == 126.0
    assert QZS5.a_km == QZS4.a_km
    assert QZS5.e == QZS4.e
