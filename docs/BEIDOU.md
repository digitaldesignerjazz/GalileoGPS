# BeiDou-Integration

BeiDou (BDS-3) ist die vierte gleichberechtigte Konstellation in GalileoGPS.  
GEO/IGSO-Satelliten helfen in Europa zwar weniger als über Asien — die MEO-Flotte (B1I/B1C) ist in Hannover trotzdem sichtbar und senkt DOP im Hybrid.

## Systemunterschiede

| Thema | GPS | BeiDou | Brücke |
|---|---|---|---|
| Zeit | GPST = UTC + 18 s | BDT = UTC + 4 s (keine Schaltsekunden seit 2006-01-01) | `timebase.py` → UTC; GPST − BDT = 14 s |
| Koordinaten | WGS84 | CGCS2000 | praktisch ITRF-nah; Ausgabe WGS84 |
| Signal | L1 C/A CDMA | B1I / B1C / B2a (BDS-3) | Talker `GB`/`BD` |
| NMEA-IDs | 1–32 | 201–237, 141–180, oder PRN 1–63 auf `GB` | `beidou_prn()` |
| Orbit | MEO | GEO + IGSO + MEO | GEO/IGSO über Europa oft flach — SNR-Filter bleibt |

## Integrationsregel

1. `GB`/`BD`-Sätze niemals als GPS lesen (PRN 1–32 wäre sonst falsch).
2. Zeiten über UTC vergleichen, nicht BDT gegen GPST roh.
3. CGCS2000 darf für Meter-PVT als WGS84-äquivalent gelten; Survey bleibt bulletin-pflichtig.
4. `beidou_sats` immer ausweisen, auch bei GPS-only-Fix.
5. `fix_type` um `beidou`, `gps-bds`, `gal-bds`, `hybrid` erweitern.

## Himmel über Hannover

Erwartbar: BDS-3-MEO mit mittlerer Elevation, GEO nahe Horizont.  
Vier nutzbare BeiDou-Sats plus GPS oder Galileo reichen für `gps-bds` / `gal-bds`. Drei Systeme → `hybrid`.
