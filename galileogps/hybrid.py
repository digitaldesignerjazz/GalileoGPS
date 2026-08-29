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
    bds = counts.get(Constellation.BEIDOU, 0)
    present = [name for name, n in (("gps", gps), ("glonass", glo), ("galileo", gal), ("beidou", bds)) if n >= 1]
    strong = [name for name, n in (("gps", gps), ("glonass", glo), ("galileo", gal), ("beidou", bds)) if n >= MIN_SATS_SINGLE]
    total = gps + glo + gal + bds

    if hdop is not None and hdop > MAX_HDOP:
        return "degraded"
    if len(strong) >= 3 or (len(present) >= 3 and total >= MIN_SATS_HYBRID):
        return "hybrid"
    if len(strong) == 2:
        pair = tuple(sorted(strong))
        return {
            ("glonass", "gps"): "gps-glo",
            ("galileo", "gps"): "gps-galileo",
            ("beidou", "gps"): "gps-bds",
            ("galileo", "glonass"): "glo-galileo",
            ("beidou", "glonass"): "glo-bds",
            ("beidou", "galileo"): "gal-bds",
        }.get(pair, "hybrid")
    if len(present) >= 2 and total >= MIN_SATS_HYBRID:
        if bds and gps:
            return "gps-bds"
        if bds and gal:
            return "gal-bds"
        if bds and glo:
            return "glo-bds"
        if gps and glo:
            return "gps-glo"
        if gps and gal:
            return "gps-galileo"
        if glo and gal:
            return "glo-galileo"
        return "hybrid"
    if gps >= MIN_SATS_SINGLE:
        return "gps"
    if glo >= MIN_SATS_SINGLE:
        return "glonass"
    if gal >= MIN_SATS_SINGLE:
        return "galileo"
    if bds >= MIN_SATS_SINGLE:
        return "beidou"
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
        "beidou_sats": int(counts.get(Constellation.BEIDOU, 0)),
        "isb_gps_glo_m": None,
        "isb_gps_bds_m": None,
        "source_talker": best.talker if best else None,
    }
