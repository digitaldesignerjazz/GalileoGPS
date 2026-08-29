from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Ecef:
    x: float
    y: float
    z: float


# Approximate 7-parameter Helmert PZ-90.11 → WGS84 (meters / mas / ppb).
# Values follow commonly published GOST / IERS-aligned sets used in GNSS
# literature. For survey-grade work replace with the current official bulletin.
PZ90_11_TO_WGS84 = {
    "dx_m": -0.013,
    "dy_m": 0.106,
    "dz_m": 0.022,
    "rx_arcsec": -0.00230,
    "ry_arcsec": 0.00354,
    "rz_arcsec": -0.00421,
    "ds_ppb": -0.008,
}


def _arcsec_to_rad(arcsec: float) -> float:
    return arcsec * (3.141592653589793 / (180.0 * 3600.0))


def pz90_11_to_wgs84(p: Ecef) -> Ecef:
    pms = PZ90_11_TO_WGS84
    rx = _arcsec_to_rad(pms["rx_arcsec"])
    ry = _arcsec_to_rad(pms["ry_arcsec"])
    rz = _arcsec_to_rad(pms["rz_arcsec"])
    m = 1.0 + pms["ds_ppb"] * 1e-9
    x = pms["dx_m"] + m * (p.x + rz * p.y - ry * p.z)
    y = pms["dy_m"] + m * (-rz * p.x + p.y + rx * p.z)
    z = pms["dz_m"] + m * (ry * p.x - rx * p.y + p.z)
    return Ecef(x, y, z)
