# GalileoGPS Architektur

Ziel: ein schlankes, mesh-fähiges Multi-GNSS-Orakel für Nexus.

## Konstellationen

- **Galileo** — EU, zivil, HAS-fähig
- **GPS** — CDMA-Rückgrat, L1 C/A
- **GLONASS** — integriert (FDMA-L1OF + Slot, Zeit- und Rahmenbrücke)
- Weitere (BeiDou, QZSS) nur als Beobachtung

## Datenfluss

1. Empfänger liefert NMEA (`GP`/`GL`/`GA`/`GN`) und/oder Raw (UBX, Android raw, RINEX)
2. Parser trennt Konstellationen — keine stillen Vermischungen
3. `timebase` zieht GPST und GLONASST auf UTC
4. `frames` zieht PZ-90.11 auf WGS84, bevor ein GLO-only/Hybrid-PVT ausgegeben wird
5. Hybrid-Klassifikator setzt `fix_type` (`gps`, `glonass`, `gps-glo`, `hybrid`, …)
6. Publisher schreibt `status/last_fix.json` und später `nxmesh` Topic `nexus/gnss/v0`

## Schnittstelle

```json
{
  "node_id": "hannover-01",
  "t_utc": "2026-08-29T17:34:00Z",
  "lat": 52.3759,
  "lon": 9.7320,
  "alt_m": 55.0,
  "fix_type": "gps-glo",
  "galileo_sats": 4,
  "gps_sats": 8,
  "glonass_sats": 7,
  "hdop": 0.82,
  "isb_gps_glo_m": null,
  "source_talker": "GN"
}
```

`glonass_sats` bleibt sichtbar, auch wenn der Fix GPS-only ist. Der Schwarm soll den Himmel sehen, nicht nur das Ergebnis.

## Hardware-Hinweise

- u-blox 8/9/10 (M8T / F9 / M10) mit GPS+GLO+GAL
- Android-Geräte mit GNSS raw measurements
- Optional Septentrio als Referenz

## Sicherheit / Privacy

Rohe Tracks bleiben lokal oder in privaten Repos.  
Das öffentliche Repository enthält nur Code, Schema und anonymisierte Beispiele.
