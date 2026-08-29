# GalileoGPS

**Multi-GNSS-Schicht (Galileo + GPS + GLONASS) für das Nexus-Ökosystem**

GalileoGPS liefert präzise Position, Geschwindigkeit und Zeit (PVT) als öffentliches Orakel für Mesh-Knoten, Agentenschwärme und Hardware-Prototypen.  
Galileo, GPS und GLONASS werden getrennt geparst und bewusst hybrid verrechnet — für Robustheit in Stadt, Feld und Mesh-Partition.

Teil von **Esslinger & Co. / Nexus**  
(neben Soilnova, Vista Nova, Lumia, York Autotype, ElysiumOS)

**Repository:** [github.com/digitaldesignerjazz/GalileoGPS](https://github.com/digitaldesignerjazz/GalileoGPS)

---

## Status

| Komponente | Lage |
|---|---|
| Repository | Public, live |
| Konstellationen | Galileo + GPS + **GLONASS** |
| NMEA-Parser (`GP`/`GL`/`GA`/`GN`) | Aktiv |
| Zeitbrücke GPST ↔ GLONASST ↔ UTC | Aktiv |
| PZ-90.11 → WGS84 | Aktiv (Helmert) |
| Hybrid-Fix (`gps-glo` / `hybrid`) | Aktiv |
| Mesh-Orakel (`nxmesh`) | Geplant |
| HAS / High Accuracy Service | Beobachtet |

---

## GPS–GLONASS-Integration

Die Brücke ist die eigentliche Arbeit — nicht das bloße Zusammenzählen von Satelliten.

1. **IDs** — GPS 1–32, GLONASS 65–96 (Slot + 64)
2. **Zeit** — GPST = UTC + 18 s, GLONASST = UTC + 3 h; Vergleich nur über UTC
3. **Rahmen** — GLONASS-Ephemeriden in PZ-90.11, Ausgabe immer WGS84
4. **Fix-Typ** — `gps`, `glonass`, `gps-glo`, `hybrid` (mit Galileo)
5. **Bias** — Feld `isb_gps_glo_m` ist vorbereitet

Details: [`docs/GPS_GLONASS.md`](docs/GPS_GLONASS.md)

---

## Schnelltest

```bash
python -m pytest tests/test_gps_glonass.py -q
```

Beispielsatz: [`samples/gps_glonass.nmea`](samples/gps_glonass.nmea) (Hannover-Nähe, GGA + GSV GPS/GLO/GAL).

```python
from pathlib import Path
from galileogps.nmea import parse_nmea_stream
from galileogps.hybrid import build_fix

snap = parse_nmea_stream(Path("samples/gps_glonass.nmea").read_text().splitlines())
print(build_fix(snap))
# fix_type: gps-glo | hybrid, glonass_sats > 0
```

---

## Architektur

```
Empfänger / NMEA / UBX
        │
   GalileoGPS Core
        │
   ├─ constellation.py   IDs, Talker, GLO-Slots
   ├─ nmea.py            GP / GL / GA / GN
   ├─ timebase.py        GPST ↔ GLONASST ↔ UTC
   ├─ frames.py          PZ-90.11 → WGS84
   ├─ hybrid.py          fix_type + last_fix Schema
   └─ Mesh Oracle        nexus/gnss/v0   (folgt)
```

---

## Schwestern-Repositories

| Repo | Rolle |
|---|---|
| [nexus](https://github.com/digitaldesignerjazz/nexus) | Integrationshub |
| [york-autotype](https://github.com/digitaldesignerjazz/york-autotype) | Heartbeat / Autonomie |
| [lumia](https://github.com/digitaldesignerjazz/lumia) | Persönliche Agentin |
| [lumina-network](https://github.com/digitaldesignerjazz/lumina-network) | Mesh-Substrat |
| [LuminaCyberspace](https://github.com/digitaldesignerjazz/LuminaCyberspace) | Swarm-Netz |

---

## Lizenz

MIT — siehe [`LICENSE`](LICENSE).  
Esslinger & Co. / Nexus Initiative · Hannover Node
