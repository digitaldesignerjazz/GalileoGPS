from pathlib import Path

from galileogps.constellation import Constellation, beidou_prn, classify_sat, glonass_slot
from galileogps.frames import Ecef, cgcs2000_to_wgs84, pz90_11_to_wgs84
from galileogps.hybrid import build_fix
from galileogps.nmea import parse_nmea_stream
from galileogps.timebase import TimeBridge


def test_ids():
    assert classify_sat(17) == Constellation.GPS
    assert classify_sat(71) == Constellation.GLONASS
    assert glonass_slot(71) == 7
    assert classify_sat(301) == Constellation.GALILEO
    assert classify_sat(201) == Constellation.BEIDOU
    assert classify_sat(12, talker="GB") == Constellation.BEIDOU
    assert beidou_prn(201) == 1
    assert beidou_prn(12, talker="GB") == 12


def test_sample_hybrid():
    sample = Path(__file__).resolve().parents[1] / "samples" / "gps_glonass.nmea"
    snap = parse_nmea_stream(sample.read_text().splitlines())
    fix = build_fix(snap, node_id="hannover-01")
    assert fix["gps_sats"] >= 4
    assert fix["glonass_sats"] >= 4
    assert fix["beidou_sats"] >= 4
    assert fix["fix_type"] in {"gps-glo", "hybrid"}
    assert fix["lat"] is not None
    assert abs(fix["lat"] - 52.3759) < 0.01


def test_time_bridge():
    tb = TimeBridge()
    assert tb.gps_minus_glonass_seconds() == 18 - 3 * 3600
    assert tb.gps_minus_bdt_seconds() == 14


def test_frame_moves_little():
    src = Ecef(3770000.0, 900000.0, 5000000.0)
    out = pz90_11_to_wgs84(src)
    assert abs(out.x - 3770000.0) < 2.0
    assert cgcs2000_to_wgs84(src) == src
