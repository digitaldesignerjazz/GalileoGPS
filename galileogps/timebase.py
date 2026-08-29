from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

GPS_UTC_LEAP_SECONDS = 18
BDT_UTC_LEAP_SECONDS = 4
GLONASS_UTC_OFFSET = timedelta(hours=3)


@dataclass
class TimeBridge:
    leap_gps_utc: int = GPS_UTC_LEAP_SECONDS
    leap_bdt_utc: int = BDT_UTC_LEAP_SECONDS

    def gps_to_utc(self, gps_datetime: datetime) -> datetime:
        if gps_datetime.tzinfo is None:
            gps_datetime = gps_datetime.replace(tzinfo=timezone.utc)
        return gps_datetime - timedelta(seconds=self.leap_gps_utc)

    def utc_to_gps(self, utc: datetime) -> datetime:
        if utc.tzinfo is None:
            utc = utc.replace(tzinfo=timezone.utc)
        return utc + timedelta(seconds=self.leap_gps_utc)

    def qzss_to_utc(self, qzss_datetime: datetime) -> datetime:
        """QZSST ≡ GPST → UTC."""
        return self.gps_to_utc(qzss_datetime)

    def utc_to_qzss(self, utc: datetime) -> datetime:
        return self.utc_to_gps(utc)

    def glonass_to_utc(self, glo_datetime: datetime) -> datetime:
        if glo_datetime.tzinfo is None:
            glo_datetime = glo_datetime.replace(tzinfo=timezone.utc)
        return glo_datetime - GLONASS_UTC_OFFSET

    def utc_to_glonass(self, utc: datetime) -> datetime:
        if utc.tzinfo is None:
            utc = utc.replace(tzinfo=timezone.utc)
        return utc + GLONASS_UTC_OFFSET

    def bdt_to_utc(self, bdt: datetime) -> datetime:
        if bdt.tzinfo is None:
            bdt = bdt.replace(tzinfo=timezone.utc)
        return bdt - timedelta(seconds=self.leap_bdt_utc)

    def utc_to_bdt(self, utc: datetime) -> datetime:
        if utc.tzinfo is None:
            utc = utc.replace(tzinfo=timezone.utc)
        return utc + timedelta(seconds=self.leap_bdt_utc)

    def gps_minus_glonass_seconds(self) -> float:
        return float(self.leap_gps_utc) - GLONASS_UTC_OFFSET.total_seconds()

    def gps_minus_bdt_seconds(self) -> float:
        return float(self.leap_gps_utc - self.leap_bdt_utc)

    def gps_minus_qzss_seconds(self) -> float:
        """QZSST is defined identical to GPST. Residual is nanoseconds, not modelled."""
        return 0.0
