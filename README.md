# GalileoGPS

**Multi-GNSS-Schicht (Galileo + GPS + GLONASS + BeiDou + QZSS) für das Nexus-Ökosystem**

GalileoGPS liefert präzise Position, Geschwindigkeit und Zeit (PVT) als öffentliches Orakel für Mesh-Knoten, Agentenschwärme und Hardware-Prototypen.  
Globale Konstellationen werden getrennt geparst; **QZSS** tritt als regionaler Asien-Augmenter hinzu.

Teil von **Esslinger & Co. / Nexus**  
(neben Soilnova, Vista Nova, Lumia, York Autotype, ElysiumOS)

**Repository:** [github.com/digitaldesignerjazz/GalileoGPS](https://github.com/digitaldesignerjazz/GalileoGPS)

---

## Status

| Komponente | Lage |
|---|---|
| Repository | Public, live |
| Konstellationen | Galileo + GPS + GLONASS + BeiDou + **QZSS (Asien)** |
| NMEA-Parser (`GP`/`GL`/`GA`/`GB`/`GQ`/`GN`) | Aktiv |
| Zeitbrücke inkl. QZSST ≡ GPST | Aktiv |
| Hybrid-Fix + `qzss_region` | Aktiv |
| Mesh-Orakel (`nxmesh`) | Geplant |
| CLAS / MADOCA (L6) | Dokumentiert, nicht in v0.4 |

---

## Konstellationsbrücken

**GPS – GLONASS** — [`docs/GPS_GLONASS.md`](docs/GPS_GLONASS.md)  
**BeiDou** — [`docs/BEIDOU.md`](docs/BEIDOU.md)  
**QZSS (Asien)** — Talker `GQ`, IDs 193–202, QZSST = GPST, Dienstbox Ost-/Südostasien + Ozeanien  
Details: [`docs/QZSS.md`](docs/QZSS.md)

Ein einziger nutzbarer QZS plus GPS ergibt `gps-qzss`. Hannover setzt `qzss_region=false`.

---

## Schnelltest

```bash
python -m pytest tests/test_gps_glonass.py -q
```

- Europa: [`samples/gps_glonass.nmea`](samples/gps_glonass.nmea) (Hannover)  
- Asien: [`samples/asia_qzss.nmea`](samples/asia_qzss.nmea) (Tokio, QZSS im Zenit)

```python
from pathlib import Path
from galileogps.nmea import parse_nmea_stream
from galileogps.hybrid import build_fix

print(build_fix(parse_nmea_stream(Path("samples/asia_qzss.nmea").read_text().splitlines()), "tokyo-01"))
# qzss_sats >= 3, qzss_region True
```

---

## Architektur

```
Empfänger / NMEA / UBX
        │
   GalileoGPS Core
        │
   ├─ constellation.py   IDs, Talker, GLO-Slots, BDS/QZSS-PRN
   ├─ nmea.py            GP / GL / GA / GB / GQ / GN
   ├─ timebase.py        GPST ≡ QZSST ↔ GLONASST ↔ BDT ↔ UTC
   ├─ frames.py          PZ-90.11 / CGCS2000 / JGD2011 → WGS84
   ├─ region.py          QZSS-Dienstbox Asien–Ozeanien
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
