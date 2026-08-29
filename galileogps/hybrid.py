from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Optional

from .constellation import Constellation
from .nmea import NmeaSnapshot

MIN_SATS_SINGLE = 4
MIN_SATS_HYBRID = 5
MAX_HDOP = 2.5


def _count_sats(snap: NmeaSnapshot) -> Counter:
    c: Counter = Counter()
    seen: set[tuple[str, int]] = set()
    for sat in snap.satellites:
        key = (sat.constellation.value, sat.nmea_id)
        if key in seen:
            continue
        seen.add(key)
        if sat.snr is None or sat.snr <= 0:
            continue
        c[sat.constellation] += 1
    return c


def _best_fix(snap: NmeaSnapshot):
    usable = [f for f in snap.fixes if f.lat is not None and f.lon is not None]
    if not usable:
        return None
    usable.sort(key=lambda f: (f.hdop is None, f.hdop or 99.0))
    return usable[0]


def classify_fix_type(counts: Counter, hdop: Optional[float]) -> str:
    gps = counts.get(Constellation.GPS, 0)
    glo = counts.get(Constellation.GLONASS, 0)
    gal = counts.get(Constellation.GALILEO, 0)
    systems = sum(1 for n in (gps, glo, gal) if n >= 1)
    total = gps + glo + gal

    if hdop is not None and hdop > MAX_HDOP:
        return "degraded"
    if gps >= MIN_SATS_SINGLE and glo >= MIN_SATS_SINGLE:
        return "gps-glo" if gal < 4 else "hybrid"
    if systems >= 2 and total >= MIN_SATS_HYBRID:
        if gal and gps and glo:
            return "hybrid"
        if gps and glo:
            return "gps-glo"
        if gps and gal:
            return "gps-galileo"
        if glo and gal:
            return "glo-galileo"
    if gps >= MIN_SATS_SINGLE:
        return "gps"
    if glo >= MIN_SATS_SINGLE:
        return "glonass"
    if gal >= MIN_SATS_SINGLE:
        return "galileo"
    return "none"


def build_fix(snap: NmeaSnapshot, node_id: str = "hannover-01") -> dict[str, Any]:
    counts = _count_sats(snap)
    best = _best_fix(snap)
    hdop = best.hdop if best else None
    fix_type = classify_fix_type(counts, hdop)
    return {
        "node_id": node_id,
        "t_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lat": best.lat if best else None,
        "lon": best.lon if best else None,
        "alt_m": best.alt_m if best else None,
        "hdop": hdop,
        "quality": best.quality if best else None,
        "fix_type": fix_type,
        "gps_sats": int(counts.get(Constellation.GPS, 0)),
        "glonass_sats": int(counts.get(Constellation.GLONASS, 0)),
        "galileo_sats": int(counts.get(Constellation.GALILEO, 0)),
        "isb_gps_glo_m": None,
        "source_talker": best.talker if best else None,
    }
