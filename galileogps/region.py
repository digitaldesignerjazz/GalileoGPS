from __future__ import annotations

from typing import Optional

# Official QZSS service is Asia-Oceania. Box is intentionally simple:
# good enough for oracle gating, not a visibility predictor.
QZSS_LAT_MIN = -35.0
QZSS_LAT_MAX = 50.0
QZSS_LON_WEST = 110.0
QZSS_LON_EAST_WRAP = -160.0  # 180° → −160° across the date line


def qzss_in_service_area(lat: Optional[float], lon: Optional[float]) -> bool:
    """True if the node sits in the QZSS Asia-Oceania service box."""
    if lat is None or lon is None:
        return False
    if not (QZSS_LAT_MIN <= lat <= QZSS_LAT_MAX):
        return False
    if lon >= QZSS_LON_WEST:
        return True
    return lon <= QZSS_LON_EAST_WRAP
