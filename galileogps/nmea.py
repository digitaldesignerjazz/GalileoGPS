from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Optional

from .constellation import TALKER_MAP, Constellation, beidou_prn, classify_sat, glonass_slot


def _checksum_ok(line: str) -> bool:
    if "*" not in line:
        return False
    body, chk = line[1:].split("*", 1)
    try:
        given = int(chk.strip()[:2], 16)
    except ValueError:
        return False
    acc = 0
    for ch in body:
        acc ^= ord(ch)
    return acc == given


@dataclass
class SatelliteView:
    nmea_id: int
    constellation: Constellation
    elevation: Optional[float] = None
    azimuth: Optional[float] = None
    snr: Optional[float] = None
    slot: Optional[int] = None
    prn: Optional[int] = None


@dataclass
class NmeaFix:
    talker: str
    sentence: str
    lat: Optional[float] = None
    lon: Optional[float] = None
    alt_m: Optional[float] = None
    quality: Optional[int] = None
    sats_used: Optional[int] = None
    hdop: Optional[float] = None
    utc: Optional[str] = None


@dataclass
class NmeaSnapshot:
    fixes: list[NmeaFix] = field(default_factory=list)
    satellites: list[SatelliteView] = field(default_factory=list)


def _dm_to_deg(dm: str, hemi: str) -> Optional[float]:
    if not dm or not hemi:
        return None
    try:
        if "." in dm:
            head, _frac = dm.split(".", 1)
        else:
            head = dm
        if len(head) <= 2:
            deg = float(dm)
        else:
            if hemi in "NS":
                n = 2
            else:
                n = 3
            deg = float(dm[:n]) + float(dm[n:]) / 60.0
        if hemi in "SW":
            deg = -deg
        return deg
    except ValueError:
        return None


def parse_nmea_line(line: str) -> Optional[dict]:
    line = line.strip()
    if not line.startswith("$") or not _checksum_ok(line):
        return None
    body = line[1:].split("*", 1)[0]
    parts = body.split(",")
    tag = parts[0]
    if len(tag) < 3:
        return None
    talker, sentence = tag[:2], tag[2:]
    return {"talker": talker, "sentence": sentence, "fields": parts[1:], "raw": line}


def _parse_gsv(talker: str, fields: list[str]) -> list[SatelliteView]:
    views: list[SatelliteView] = []
    chunks = fields[3:]
    for i in range(0, len(chunks), 4):
        group = chunks[i : i + 4]
        if not group or not group[0]:
            continue
        try:
            sat_id = int(group[0])
        except ValueError:
            continue
        mapped = TALKER_MAP.get(talker)
        const = mapped if mapped is not None else classify_sat(sat_id, talker=talker)

        def _f(idx: int) -> Optional[float]:
            if idx >= len(group) or group[idx] == "":
                return None
            try:
                return float(group[idx])
            except ValueError:
                return None

        views.append(
            SatelliteView(
                nmea_id=sat_id,
                constellation=const,
                elevation=_f(1),
                azimuth=_f(2),
                snr=_f(3),
                slot=glonass_slot(sat_id) if const == Constellation.GLONASS else None,
                prn=beidou_prn(sat_id, talker) if const == Constellation.BEIDOU else None,
            )
        )
    return views


def _parse_gga(talker: str, fields: list[str]) -> NmeaFix:
    lat = _dm_to_deg(fields[1], fields[2]) if len(fields) > 2 else None
    lon = _dm_to_deg(fields[3], fields[4]) if len(fields) > 4 else None

    def _i(idx: int) -> Optional[int]:
        if idx >= len(fields) or fields[idx] == "":
            return None
        try:
            return int(fields[idx])
        except ValueError:
            return None

    def _fl(idx: int) -> Optional[float]:
        if idx >= len(fields) or fields[idx] == "":
            return None
        try:
            return float(fields[idx])
        except ValueError:
            return None

    return NmeaFix(
        talker=talker,
        sentence="GGA",
        utc=fields[0] if fields else None,
        lat=lat,
        lon=lon,
        quality=_i(5),
        sats_used=_i(6),
        hdop=_fl(7),
        alt_m=_fl(8),
    )


def parse_nmea_stream(lines: Iterable[str]) -> NmeaSnapshot:
    snap = NmeaSnapshot()
    for line in lines:
        parsed = parse_nmea_line(line)
        if not parsed:
            continue
        talker, sentence, fields = parsed["talker"], parsed["sentence"], parsed["fields"]
        if sentence == "GSV":
            snap.satellites.extend(_parse_gsv(talker, fields))
        elif sentence == "GGA":
            snap.fixes.append(_parse_gga(talker, fields))
    return snap
