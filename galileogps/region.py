from __future__ import annotations

# Official QZSS service is Asia-Oceania. Box is intentionally simple:
# good enough for oracle gating, not a visibility predictor.
QZSS_LAT_MIN = -35.0
QZSS_LAT_MAX = 50.0
QZSS_LON_MIN = 110.0
QZSS_LON_MAX = 180.0
QZSS_LON_WRAP_WEST = -160.0  # central/eastern Pacific edge


def qzss_in_service_area(lat: float | None, lon: float | None) -> bool:
    """True if the node sits in the QZSS Asia-Oceania service box."""
    if lat is None or lon is None:
        return False
    if not (QZSS_LAT_MIN <= lat <= QZSS_LAT_MAX):
        return False
    if QZSS_LON_MIN <= lon <= QZSS_LON_MAX:
        return True
    if lon >= QZSS_LON_WRAP_WEST and lon < -180 + 1e-9:
        return False
    return lon >= QZSS_LON_WRAP_WEST
