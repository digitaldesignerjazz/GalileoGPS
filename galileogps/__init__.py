"""GalileoGPS — Multi-GNSS core for the Nexus ecosystem."""

from .constellation import classify_sat, Constellation
from .nmea import parse_nmea_line, parse_nmea_stream
from .hybrid import build_fix

__all__ = [
    "Constellation",
    "classify_sat",
    "parse_nmea_line",
    "parse_nmea_stream",
    "build_fix",
]

__version__ = "0.2.0"
