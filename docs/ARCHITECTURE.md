# GalileoGPS Architektur

Ziel: ein schlankes, mesh-fähiges Multi-GNSS-Orakel für Nexus.

## Konstellationen

- **Galileo** — primär (EU, zivil, HAS-fähig)
- **GPS** — sekundär / Hybrid-Fix
- Weitere (GLONASS, BeiDou, QZSS) nur als Beobachtung, nicht als Kernpflicht

## Datenfluss

1. Empfänger liefert NMEA und/oder Raw (u-blox UBX, Android GNSS raw, RINEX)
2. Parser normalisiert Satelliten, SNR, Ephemeriden-Alter, Zeit
3. PVT-Schätzer erzeugt Fix + Unsicherheit + DOP
4. Health-Monitor vergleicht Galileo-only vs. GPS-only vs. Hybrid
5. Publisher schreibt `status/last_fix.json` und optional `nxmesh` Topic `nexus/gnss/v0`

## Schnittstelle (Entwurf)

```json
{
  "node_id": "hannover-01",
  "t_utc": "2026-08-29T17:34:00Z",
  "lat": 52.3759,
  "lon": 9.7320,
  "alt_m": 55.0,
  "fix_type": "hybrid",
  "galileo_sats": 9,
  "gps_sats": 8,
  "hdop": 0.8,
  "age_s": 1.2
}
```

## Hardware-Hinweise

Bevorzugt getestet werden sollen:

- u-blox 8/9/10 (M8T / F9 / M10)
- Android-Geräte mit GNSS raw measurements
- Optional Septentrio für Referenz

## Sicherheit / Privacy

Rohe Tracks bleiben lokal oder in privaten Repos.  
Das öffentliche Repository enthält nur Code, Schema und anonymisierte Beispiele.
