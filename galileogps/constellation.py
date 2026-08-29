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


def classify_sat(nmea_id: int, talker: Optional[str] = None) -> Constellation:
    """Map NMEA satellite IDs to a constellation.

    Talker wins when the sentence is system-specific:
    - GB / BD + PRN 1–63 → BeiDou (nicht GPS)
    - GA + 1–36 → Galileo

    Numeric fallback (u-blox / NMEA 4.10 / 4.11):
    - GPS     1–32
    - SBAS    33–64
    - GLONASS 65–96
    - QZSS    193–199
    - BeiDou  141–180, 201–237, 401+
    - Galileo 301–336
    """
    if talker in ("GB", "BD"):
        return Constellation.BEIDOU
    if talker == "GA":
        return Constellation.GALILEO
    if talker == "GL":
        return Constellation.GLONASS
    if talker == "GP":
        return Constellation.GPS
    if talker == "GQ":
        return Constellation.QZSS

    if 65 <= nmea_id <= 96:
        return Constellation.GLONASS
    if 301 <= nmea_id <= 336:
        return Constellation.GALILEO
    if 193 <= nmea_id <= 199:
        return Constellation.QZSS
    if 141 <= nmea_id <= 180 or 201 <= nmea_id <= 237 or nmea_id >= 401:
        return Constellation.BEIDOU
    if 1 <= nmea_id <= 32:
        return Constellation.GPS
    return Constellation.UNKNOWN


def glonass_slot(nmea_id: int) -> Optional[int]:
    """Return GLONASS orbital slot (1–24) from NMEA ID 65–96."""
    if 65 <= nmea_id <= 96:
        slot = nmea_id - 64
        if 1 <= slot <= 24:
            return slot
    return None


def beidou_prn(nmea_id: int, talker: Optional[str] = None) -> Optional[int]:
    """Normalize a NMEA ID to BeiDou PRN (C01…).

    - GB/BD talker: ID is already the PRN
    - 201–237 → PRN = ID − 200
    - 141–180 → PRN = ID − 140
    - 401+ → PRN = ID − 400
    """
    if talker in ("GB", "BD") and 1 <= nmea_id <= 63:
        return nmea_id
    if 201 <= nmea_id <= 237:
        return nmea_id - 200
    if 141 <= nmea_id <= 180:
        return nmea_id - 140
    if nmea_id >= 401:
        return nmea_id - 400
    return None
