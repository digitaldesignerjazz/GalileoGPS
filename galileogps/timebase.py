from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

# GPS-UTC leap seconds. Update when IERS / GNSS ICD announces a new leap second.
# Last inserted leap second: 2016-12-31. Valid for 2026 operations.
GPS_UTC_LEAP_SECONDS = 18

# GLONASS time is aligned to Moscow time scale: GLONASST = UTC + 3 hours
# (no GPS-style leap-second offset inside the GLO timescale itself).
GLONASS_UTC_OFFSET = timedelta(hours=3)


@dataclass
class TimeBridge:
    leap_gps_utc: int = GPS_UTC_LEAP_SECONDS

    def gps_to_utc(self, gps_datetime: datetime) -> datetime:
        """GPST → UTC. Input naive or aware; output UTC-aware."""
        if gps_datetime.tzinfo is None:
            gps_datetime = gps_datetime.replace(tzinfo=timezone.utc)
        return gps_datetime - timedelta(seconds=self.leap_gps_utc)

    def utc_to_gps(self, utc: datetime) -> datetime:
        if utc.tzinfo is None:
            utc = utc.replace(tzinfo=timezone.utc)
        return utc + timedelta(seconds=self.leap_gps_utc)

    def glonass_to_utc(self, glo_datetime: datetime) -> datetime:
        """GLONASST → UTC (subtract 3 hours)."""
        if glo_datetime.tzinfo is None:
            glo_datetime = glo_datetime.replace(tzinfo=timezone.utc)
        return glo_datetime - GLONASS_UTC_OFFSET

    def utc_to_glonass(self, utc: datetime) -> datetime:
        if utc.tzinfo is None:
            utc = utc.replace(tzinfo=timezone.utc)
        return utc + GLONASS_UTC_OFFSET

    def gps_minus_glonass_seconds(self) -> float:
        """Nominal GPST − GLONASST at the same instant, in seconds.

        GPST = UTC + 18 s
        GLONASST = UTC + 3 h
        ⇒ GPST − GLONASST = 18 − 10800 = −10782 s
        Receiver firmware usually hides this; raw PVT must not.
        """
        return float(self.leap_gps_utc) - GLONASS_UTC_OFFSET.total_seconds()
