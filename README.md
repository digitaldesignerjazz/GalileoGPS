# GalileoGPS

**Multi-GNSS-Schicht (Galileo + GPS + GLONASS + BeiDou) für das Nexus-Ökosystem**

GalileoGPS liefert präzise Position, Geschwindigkeit und Zeit (PVT) als öffentliches Orakel für Mesh-Knoten, Agentenschwärme und Hardware-Prototypen.  
Die vier Konstellationen werden getrennt geparst und bewusst hybrid verrechnet — für Robustheit in Stadt, Feld und Mesh-Partition.

Teil von **Esslinger & Co. / Nexus**  
(neben Soilnova, Vista Nova, Lumia, York Autotype, ElysiumOS)

**Repository:** [github.com/digitaldesignerjazz/GalileoGPS](https://github.com/digitaldesignerjazz/GalileoGPS)

---

## Status

| Komponente | Lage |
|---|---|
| Repository | Public, live |
| Konstellationen | Galileo + GPS + GLONASS + **BeiDou** |
| NMEA-Parser (`GP`/`GL`/`GA`/`GB`/`BD`/`GN`) | Aktiv |
| Zeitbrücke GPST ↔ GLONASST ↔ BDT ↔ UTC | Aktiv |
| PZ-90.11 → WGS84 | Aktiv (Helmert) |
| CGCS2000 → WGS84 | Aktiv (Meter-Äquivalenz) |
| Hybrid-Fix (`gps-glo` / `gps-bds` / `hybrid`) | Aktiv |
| Mesh-Orakel (`nxmesh`) | Geplant |
| HAS / High Accuracy Service | Beobachtet |

---

## Konstellationsbrücken

Die Arbeit sitzt in den Brücken — nicht im Zusammenzählen.

**GPS – GLONASS** — IDs 65–96, GLONASST = UTC + 3 h, PZ-90.11 → WGS84  
Details: [`docs/GPS_GLONASS.md`](docs/GPS_GLONASS.md)

**BeiDou** — Talker `GB`/`BD`, IDs 201–237 / PRN auf GB, BDT = UTC + 4 s, GPST − BDT = 14 s, CGCS2000 ≈ WGS84  
Details: [`docs/BEIDOU.md`](docs/BEIDOU.md)

`fix_type` u. a.: `gps`, `glonass`, `galileo`, `beidou`, `gps-glo`, `gps-bds`, `gal-bds`, `hybrid`.

---

## Schnelltest

```bash
python -m pytest tests/test_gps_glonass.py -q
```

Beispielsatz: [`samples/gps_glonass.nmea`](samples/gps_glonass.nmea) (Hannover-Nähe, GGA + GSV GPS/GLO/GAL/BDS).

```python
from pathlib import Path
from galileogps.nmea import parse_nmea_stream
from galileogps.hybrid import build_fix

snap = parse_nmea_stream(Path("samples/gps_glonass.nmea").read_text().splitlines())
print(build_fix(snap))
# beidou_sats > 0, fix_type oft hybrid
```

---

## Architektur

```
Empfänger / NMEA / UBX
        │
   GalileoGPS Core
        │
   ├─ constellation.py   IDs, Talker, GLO-Slots, BDS-PRN
   ├─ nmea.py            GP / GL / GA / GB / BD / GN
   ├─ timebase.py        GPST ↔ GLONASST ↔ BDT ↔ UTC
   ├─ frames.py          PZ-90.11 / CGCS2000 → WGS84
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
