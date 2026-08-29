"""GalileoGPS — Multi-GNSS core for the Nexus ecosystem."""

from .constellation import Constellation, beidou_prn, classify_sat, qzss_prn
from .hybrid import build_fix
from .nmea import parse_nmea_line, parse_nmea_stream
from .qzss_orbits import QZS4, QZS5, get_slot
from .region import qzss_in_service_area

__all__ = [
    "Constellation",
    "classify_sat",
    "beidou_prn",
    "qzss_prn",
    "qzss_in_service_area",
    "QZS4",
    "QZS5",
    "get_slot",
    "parse_nmea_line",
    "parse_nmea_stream",
    "build_fix",
]

__version__ = "0.4.1"
