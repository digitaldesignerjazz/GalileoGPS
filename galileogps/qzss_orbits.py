from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

EARTH_RADIUS_KM = 6378.137


@dataclass(frozen=True)
class QzoSlot:
    name: str
    svn: Optional[int]
    prn_pnt: Optional[int]
    norad: Optional[int]
    cospar: Optional[str]
    block: str
    orbit_class: str  # QZO | GEO | QGEO
    status: str  # operational | lost | planned | commissioning
    a_km: float
    e: float
    i_deg: float
    omega_deg: float
    raan_deg: Optional[float]
    lambda_east_deg: Optional[float]
    raan_epoch: Optional[str] = None
    notes: str = ""

    @property
    def perigee_alt_km(self) -> float:
        return self.a_km * (1.0 - self.e) - EARTH_RADIUS_KM

    @property
    def apogee_alt_km(self) -> float:
        return self.a_km * (1.0 + self.e) - EARTH_RADIUS_KM


# Nominal QZO from PS-QZSS-005 Table 3.2-4 (Cabinet Office).
# QZS-5 launch failed 2025-12-22 (H3 F8); slot remains the published design.
QZS4 = QzoSlot(
    name="QZS-4",
    svn=4,
    prn_pnt=195,
    norad=42965,
    cospar="2017-062A",
    block="II-Q",
    orbit_class="QZO",
    status="operational",
    a_km=42165.0,
    e=0.075,
    i_deg=41.0,
    omega_deg=270.0,
    raan_deg=347.0,
    lambda_east_deg=137.5,
    raan_epoch="2025-09",
    notes="Center longitude 132.0–142.5 E. Inclination 41±5. Launched 2017-10-10 H-IIA.",
)

QZS5 = QzoSlot(
    name="QZS-5",
    svn=6,
    prn_pnt=None,
    norad=None,
    cospar=None,
    block="III-Q",
    orbit_class="QZO",
    status="lost",
    a_km=42165.0,
    e=0.075,
    i_deg=41.0,
    omega_deg=270.0,
    raan_deg=126.0,
    lambda_east_deg=139.0,
    raan_epoch="2031-10",
    notes=(
        "Design slot only. H3-22S launch failure 2025-12-22. "
        "CAO: six-satellite ops without QZS-5. Replacement targeted ~2027. "
        "Intended λ = 139±5.5 E, RAAN mid-life 126 deg."
    ),
)

QZO_CATALOG = {"QZS-4": QZS4, "QZS-5": QZS5}


def get_slot(name: str) -> QzoSlot:
    return QZO_CATALOG[name]
