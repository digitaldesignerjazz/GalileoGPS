# GPS–GLONASS-Integration

GalileoGPS behandelt GPS und GLONASS als **gleichberechtigte** Konstellationen im Hybrid-Fix. Galileo bleibt dritte Säule; dieser Text beschreibt nur die GPS–GLO-Brücke.

## Warum beide

- GPS: globales CDMA-Rückgrat, L1 C/A überall verfügbar
- GLONASS: andere Orbitgeometrie (höhere Inklination), oft bessere Sichtbarkeit in mittleren/hohen Breiten (Hannover)
- Hybrid senkt DOP in Straßenschluchten und unter Teilabschattung

## Systemunterschiede, die der Kern ausgleichen muss

| Thema | GPS | GLONASS | Brücke in GalileoGPS |
|---|---|---|---|
| Zeit | GPST = UTC + Leap Seconds | GLONASST ≈ UTC + 3 h (ohne GPS-Schaltsekundenlogik) | `timebase.py` → gemeinsame UTC |
| Koordinaten | WGS84 | PZ-90.11 | `frames.py` → WGS84 |
| Signal | CDMA, PRN 1–32 | historisch FDMA L1OF (Kanal −7…+6), neuer CDMA | Kanal + Slot merken, nicht nur PRN |
| NMEA-Talker | `GP` | `GL` | `GN` = kombiniert |
| Sat-ID in GSV | 1–32 | üblich 65–96 (Slot + 64) | `constellation.py` |
| Bias | — | Inter-System Bias + Inter-Frequency Bias | `isb_gps_glo` im Fix |

## NMEA, die zählt

- `$GPGGA` / `$GLGGA` / `$GNGGA` — Fix, Qualität, Sat-Anzahl
- `$GPGSV` / `$GLGSV` / `$GAGSV` — Sichtbarkeit je Konstellation
- `$GNRMC` — kombinierte Navigation
- `$GNGSA` — DOP und benutzte Sats (Systeme über Feld 1 / System-ID)

Roh-UBX (`NAV-PVT`, `NAV-SAT`, `RXM-RAWX`) bleibt der bevorzugte Pfad, sobald ein u-blox hängt.

## Integrationsregel

1. Jede Konstellation separat parsen (keine stillen Vermischungen).
2. Zeiten auf UTC bringen, bevor Position verrechnet wird.
3. PZ-90.11 → WGS84 nur bei GLO-only oder gemischtem PVT aus Ephemeriden.
4. Hybrid-Fix nur, wenn **beide** Systeme mindestens 4 brauchbare Sats *oder* zusammen ≥ 5 mit akzeptablem HDOP liefern.
5. `fix_type` ausweisen: `gps`, `glonass`, `galileo`, `gps-glo`, `hybrid`.

## Mesh-Orakel

Topic: `nexus/gnss/v0`  
Feld `glonass_sats` ist Pflicht, sobald ein GLO-Satz gesehen wurde — auch wenn der Fix GPS-only bleibt. So sieht der Schwarm die wahre Himmelssicht über Hannover.
