# GalileoGPS Architektur

Ziel: ein schlankes, mesh-fähiges Multi-GNSS-Orakel für Nexus.

## Konstellationen

- **Galileo** — EU, zivil, HAS-fähig
- **GPS** — CDMA-Rückgrat, L1 C/A
- **GLONASS** — integriert (FDMA-L1OF + Slot, Zeit- und Rahmenbrücke)
- **BeiDou** — integriert (BDS-3 MEO/IGSO/GEO, BDT, CGCS2000)
- QZSS nur als Beobachtung

## Datenfluss

1. Empfänger liefert NMEA (`GP`/`GL`/`GA`/`GB`/`BD`/`GN`) und/oder Raw (UBX, Android raw, RINEX)
2. Parser trennt Konstellationen — `GB`/`BD` darf niemals als GPS gelesen werden
3. `timebase` zieht GPST, GLONASST und BDT auf UTC
4. `frames` zieht PZ-90.11 und CGCS2000 auf WGS84
5. Hybrid-Klassifikator setzt `fix_type` (`gps`, `glonass`, `galileo`, `beidou`, `gps-glo`, `gps-bds`, `hybrid`, …)
6. Publisher schreibt `status/last_fix.json` und später `nxmesh` Topic `nexus/gnss/v0`

## Schnittstelle

```json
{
  "node_id": "hannover-01",
  "t_utc": "2026-08-29T17:40:00Z",
  "lat": 52.3759,
  "lon": 9.7320,
  "alt_m": 55.0,
  "fix_type": "hybrid",
  "galileo_sats": 4,
  "gps_sats": 8,
  "glonass_sats": 7,
  "beidou_sats": 8,
  "hdop": 0.82,
  "isb_gps_glo_m": null,
  "isb_gps_bds_m": null,
  "source_talker": "GN"
}
```

`beidou_sats` und `glonass_sats` bleiben sichtbar, auch wenn der Fix GPS-only ist.

## Hardware-Hinweise

- u-blox F9 / M10 mit GPS+GLO+GAL+BDS
- Android-Geräte mit GNSS raw measurements
- Optional Septentrio als Referenz

## Sicherheit / Privacy

Rohe Tracks bleiben lokal oder in privaten Repos.  
Das öffentliche Repository enthält nur Code, Schema und anonymisierte Beispiele.
