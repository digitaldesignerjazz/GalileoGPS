from __future__ import annotations

from enum import Enum
from typing import Optional


class Constellation(str, Enum):
    GPS = "gps"
    GLONASS = "glonass"
    GALILEO = "galileo"
    BEIDOU = "beidou"
    QZSS = "qzss"
    UNKNOWN = "unknown"


# NMEA talker → constellation
TALKER_MAP = {
    "GP": Constellation.GPS,
    "GL": Constellation.GLONASS,
    "GA": Constellation.GALILEO,
    "GB": Constellation.BEIDOU,
    "BD": Constellation.BEIDOU,
    "GQ": Constellation.QZSS,
    "GN": None,  # combined / multi-GNSS
}


def classify_sat(nmea_id: int) -> Constellation:
    """Map common NMEA satellite IDs to a constellation.

    Conventional civilian mapping (u-blox / NMEA 4.1 style):
    - GPS     1–32
    - SBAS    33–64
    - GLONASS 65–96   (slot + 64)
    - Galileo 301–336 or 1–36 on GA talker
    - BeiDou  201–235 / 401+
    """
    if 1 <= nmea_id <= 32:
        return Constellation.GPS
    if 65 <= nmea_id <= 96:
        return Constellation.GLONASS
    if 301 <= nmea_id <= 336:
        return Constellation.GALILEO
    if 193 <= nmea_id <= 202:
        return Constellation.QZSS
    if 201 <= nmea_id <= 235 or nmea_id >= 401:
        return Constellation.BEIDOU
    return Constellation.UNKNOWN


def glonass_slot(nmea_id: int) -> Optional[int]:
    """Return GLONASS orbital slot (1–24) from NMEA ID 65–96."""
    if 65 <= nmea_id <= 96:
        slot = nmea_id - 64
        if 1 <= slot <= 24:
            return slot
    return None
