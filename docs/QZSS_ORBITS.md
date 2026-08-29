# QZS-4 / QZS-5 Orbit

Quelle der Sollbahn: Cabinet Office **PS-QZSS-005**, Tabelle 3.2-4.  
Status QZS-5: **QSS-CUS-101439** (Sechs-Satelliten-Betrieb nach Verlust).

Beide Slots sind **QZO** — Tundra-nahe, leicht elliptische geosynchrone Bahnen. Der Boden-Track ist eine unsymmetrische Acht über Asien; Apogäum liegt über der Nordhemisphäre, deshalb steht der Satellit lange hoch über Japan.

## Gemeinsame QZO-Geometrie

| Größe | Soll |
|---|---|
| Bahnklasse | QZO (inclined geosynchronous, eccentric) |
| Große Halbachse *a* | 42 165 km |
| Exzentrizität *e* | 0,075 ± 0,015 |
| Inklination *i* | 41° (Mittel über 15 Jahre), Band 41° ± 5° |
| Argument des Perigäums *ω* | 270° ± 2,5° |
| Umlauf | 1 siderealer Tag (≈ 23 h 56 min) |
| Perigäumshöhe | ≈ 32 625 km |
| Apogäumshöhe | ≈ 38 949 km |

Perigäum südlich, Apogäum nördlich — das ist der Zenit-Trick über Japan.

## QZS-4 — aktiv

| | |
|---|---|
| Name | QZS-4 / Michibiki-4 |
| Status | operational (CAO 2026-08-25) |
| Block | II-Q |
| SVN / PNT-PRN | 004 / **195** |
| NORAD / COSPAR | 42965 / 2017-062A |
| Start | 2017-10-10, H-IIA 202 |
| *Ω* (Mitte der Nutzungsdauer) | **347°** (Epoche September 2025) |
| Zentrumslänge *λ* | **137,5° Ost** (Mittel über ~6 Monate) |
| *λ*-Fenster | 132,0° … 142,5° Ost |
| Signale | L1 C/A, L1C, L2C, L5, L1S, L5S, L6D, L6E |

Gemessene TLE-Nähe (Ende 2025): *i* ≈ 40,22°, *e* ≈ 0,07515, *ω* ≈ 271,7° — innerhalb der PS-QZSS-Bänder.

## QZS-5 — verloren, Sollbahn bleibt der Slot

| | |
|---|---|
| Name | QZS-5 / Michibiki-5 |
| Status | **lost** — H3-22S (F8), 2025-12-22, Zweitstufenfehler |
| Block | III-Q (geplant) |
| Bahnklasse | QZO (gleiche Familie wie QZS-2 / 4 / 1R) |
| *Ω* (Mitte der Nutzungsdauer) | **126°** (Epoche Oktober 2031) |
| Zentrumslänge *λ* | **139,0° Ost** |
| *λ*-Fenster | 139° ± 5,5° |
| Ersatz | CAO: Sechs-Satelliten-Betrieb (QZS-2, -3, -4, -1R, -6, -7); Ersatzstart anvisiert ~2027 |

QZS-5 sollte die vierte QZO-Maschine werden, damit über Japan dauerhaft ein QZO-Satellit im hohen Elevationsfenster steht. Ohne ihn bleibt die 7er-Konstellation unvollständig; PNT läuft weiter über GPS+QZSS-Hybrid.

## Sichtbarkeit Asien

- **QZS-4** zeichnet die Acht um ~137,5° E — Tokio, Seoul, Taipei liegen unter dem nördlichen Bogen.
- **QZS-5** hätte dieselbe Acht um ~139° E gelegt, 120° RAAN-Versatz zu anderen QZO-Slots.
- Hannover liegt außerhalb; `qzss_region` bleibt falsch.

Code: `galileogps.qzss_orbits.QZS4` / `QZS5`.
