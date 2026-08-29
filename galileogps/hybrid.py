from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from typing import Any, Optional

from .constellation import Constellation
from .nmea import NmeaSnapshot
from .region import qzss_in_service_area

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
    qzss = counts.get(Constellation.QZSS, 0)
    present = [
        name
        for name, n in (
            ("gps", gps),
            ("glonass", glo),
            ("galileo", gal),
            ("beidou", bds),
        )
        if n >= 1
    ]
    strong = [
        name
        for name, n in (
            ("gps", gps),
            ("glonass", glo),
            ("galileo", gal),
            ("beidou", bds),
        )
        if n >= MIN_SATS_SINGLE
    ]
    total = gps + glo + gal + bds + qzss

    if hdop is not None and hdop > MAX_HDOP:
        return "degraded"
    if len(strong) >= 3 or (len(present) >= 3 and total >= MIN_SATS_HYBRID):
        return "hybrid"
    if qzss >= 1 and gps >= MIN_SATS_SINGLE and len(strong) <= 1:
        return "gps-qzss"
    if len(strong) == 2:
        pair = tuple(sorted(strong))
        label = {
            ("glonass", "gps"): "gps-glo",
            ("galileo", "gps"): "gps-galileo",
            ("beidou", "gps"): "gps-bds",
            ("galileo", "glonass"): "glo-galileo",
            ("beidou", "glonass"): "glo-bds",
            ("beidou", "galileo"): "gal-bds",
        }.get(pair, "hybrid")
        if qzss and label.startswith("gps"):
            return "hybrid" if label != "gps-qzss" else label
        return label
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
        if gps and qzss:
            return "gps-qzss"
        return "hybrid"
    if gps >= MIN_SATS_SINGLE:
        return "gps-qzss" if qzss else "gps"
    if glo >= MIN_SATS_SINGLE:
        return "glonass"
    if gal >= MIN_SATS_SINGLE:
        return "galileo"
    if bds >= MIN_SATS_SINGLE:
        return "beidou"
    if qzss >= 1:
        return "qzss-only"
    return "none"


def build_fix(snap: NmeaSnapshot, node_id: str = "hannover-01") -> dict[str, Any]:
    counts = _count_sats(snap)
    best = _best_fix(snap)
    hdop = best.hdop if best else None
    fix_type = classify_fix_type(counts, hdop)
    lat = best.lat if best else None
    lon = best.lon if best else None
    return {
        "node_id": node_id,
        "t_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "lat": lat,
        "lon": lon,
        "alt_m": best.alt_m if best else None,
        "hdop": hdop,
        "quality": best.quality if best else None,
        "fix_type": fix_type,
        "gps_sats": int(counts.get(Constellation.GPS, 0)),
        "glonass_sats": int(counts.get(Constellation.GLONASS, 0)),
        "galileo_sats": int(counts.get(Constellation.GALILEO, 0)),
        "beidou_sats": int(counts.get(Constellation.BEIDOU, 0)),
        "qzss_sats": int(counts.get(Constellation.QZSS, 0)),
        "qzss_region": qzss_in_service_area(lat, lon),
        "isb_gps_glo_m": None,
        "isb_gps_bds_m": None,
        "isb_gps_qzss_m": 0.0,
        "source_talker": best.talker if best else None,
    }
