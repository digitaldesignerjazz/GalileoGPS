# GalileoGPS Architektur

Ziel: ein schlankes, mesh-fähiges Multi-GNSS-Orakel für Nexus.

## Konstellationen

- **Galileo** — EU, zivil, HAS-fähig
- **GPS** — CDMA-Rückgrat, L1 C/A
- **GLONASS** — integriert (FDMA-L1OF + Slot)
- **BeiDou** — integriert (BDS-3, BDT, CGCS2000)
- **QZSS** — regionaler Asien-Augmenter (GQ, QZSST ≡ GPST, JGD2011)

## Datenfluss

1. Empfänger liefert NMEA (`GP`/`GL`/`GA`/`GB`/`GQ`/`GN`) und/oder Raw
2. Parser trennt Konstellationen — `GQ` niemals als GPS
3. `timebase` zieht alle Skalen auf UTC (QZSS = GPS)
4. `region.qzss_in_service_area` markiert Asien–Ozeanien
5. Hybrid-Klassifikator: schon 1 QZS + GPS → `gps-qzss`
6. Publisher schreibt `status/last_fix.json` / später `nexus/gnss/v0`

## Schnittstelle

```json
{
  "node_id": "tokyo-01",
  "t_utc": "2026-08-29T10:45:00Z",
  "lat": 35.6762,
  "lon": 139.6503,
  "alt_m": 40.1,
  "fix_type": "hybrid",
  "gps_sats": 8,
  "qzss_sats": 4,
  "beidou_sats": 6,
  "qzss_region": true,
  "isb_gps_qzss_m": 0.0,
  "source_talker": "GN"
}
```

Hannover: `qzss_region=false`, `qzss_sats` trotzdem sichtbar falls ein Satz ankommt.

## Hardware-Hinweise

- u-blox F9 / M10 mit GPS+GLO+GAL+BDS+QZSS (Asien-Knoten)
- Android GNSS raw
- Optional Septentrio

## Sicherheit / Privacy

Rohe Tracks bleiben lokal oder privat. Öffentlich nur Code, Schema, anonymisierte Beispiele.
