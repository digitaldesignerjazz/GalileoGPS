from pathlib import Path

from galileogps.constellation import Constellation, beidou_prn, classify_sat, glonass_slot, qzss_prn
from galileogps.frames import Ecef, cgcs2000_to_wgs84, jgd2011_to_wgs84, pz90_11_to_wgs84
from galileogps.hybrid import build_fix
from galileogps.nmea import parse_nmea_stream
from galileogps.region import qzss_in_service_area
from galileogps.timebase import TimeBridge

ROOT = Path(__file__).resolve().parents[1]


def test_ids():
    assert classify_sat(17) == Constellation.GPS
    assert classify_sat(71) == Constellation.GLONASS
    assert glonass_slot(71) == 7
    assert classify_sat(301) == Constellation.GALILEO
    assert classify_sat(201) == Constellation.BEIDOU
    assert classify_sat(12, talker="GB") == Constellation.BEIDOU
    assert classify_sat(193) == Constellation.QZSS
    assert classify_sat(1, talker="GQ") == Constellation.QZSS
    assert beidou_prn(201) == 1
    assert qzss_prn(193) == 193
    assert qzss_prn(1, talker="GQ") == 193


def test_sample_hybrid():
    snap = parse_nmea_stream((ROOT / "samples" / "gps_glonass.nmea").read_text().splitlines())
    fix = build_fix(snap, node_id="hannover-01")
    assert fix["gps_sats"] >= 4
    assert fix["glonass_sats"] >= 4
    assert fix["beidou_sats"] >= 4
    assert fix["qzss_sats"] == 0
    assert fix["qzss_region"] is False
    assert fix["fix_type"] in {"gps-glo", "hybrid"}
    assert abs(fix["lat"] - 52.3759) < 0.01


def test_asia_qzss():
    snap = parse_nmea_stream((ROOT / "samples" / "asia_qzss.nmea").read_text().splitlines())
    fix = build_fix(snap, node_id="tokyo-01")
    assert fix["qzss_sats"] >= 3
    assert fix["gps_sats"] >= 4
    assert fix["qzss_region"] is True
    assert abs(fix["lat"] - 35.6762) < 0.01
    assert abs(fix["lon"] - 139.6503) < 0.01
    assert fix["fix_type"] in {"gps-qzss", "gps-bds", "hybrid"}


def test_qzss_region_box():
    assert qzss_in_service_area(35.68, 139.65) is True   # Tokyo
    assert qzss_in_service_area(1.35, 103.8) is False    # Singapore slightly west of 110
    assert qzss_in_service_area(-33.87, 151.21) is True  # Sydney
    assert qzss_in_service_area(52.38, 9.73) is False    # Hannover


def test_time_bridge():
    tb = TimeBridge()
    assert tb.gps_minus_glonass_seconds() == 18 - 3 * 3600
    assert tb.gps_minus_bdt_seconds() == 14
    assert tb.gps_minus_qzss_seconds() == 0.0


def test_frame_moves_little():
    src = Ecef(3770000.0, 900000.0, 5000000.0)
    assert abs(pz90_11_to_wgs84(src).x - 3770000.0) < 2.0
    assert cgcs2000_to_wgs84(src) == src
    assert jgd2011_to_wgs84(src) == src
