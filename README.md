# GalileoGPS

**Multi-GNSS-Schicht (Galileo + GPS) für das Nexus-Ökosystem**

GalileoGPS liefert präzise Position, Geschwindigkeit und Zeit (PVT) als öffentliches Orakel für Mesh-Knoten, Agentenschwärme und Hardware-Prototypen.  
Europäisches Galileo und US-GPS werden gemeinsam ausgewertet — für Robustheit in Stadt, Feld und Mesh-Partition.

Teil von **Esslinger & Co. / Nexus**  
(neben Soilnova, Vista Nova, Lumia, York Autotype, ElysiumOS)

**Repository:** [github.com/digitaldesignerjazz/GalileoGPS](https://github.com/digitaldesignerjazz/GalileoGPS)

---

## Status

| Komponente | Lage |
|---|---|
| Repository | Public, live |
| Konstellationen | Galileo (E1/E5 geplant) + GPS (L1 C/A) |
| PVT-Kern | Geplant |
| Mesh-Orakel (`nxmesh`) | Geplant |
| HAS / High Accuracy Service | Beobachtet |
| Agenten-Anbindung (Lyra / Xen / Elara / Lumia) | Geplant |

---

## Auftrag

1. **Ort** — belastbare Koordinaten für Hannover-Node und mobile Prototypen  
2. **Zeit** — GNSS-Zeit als gemeinsame Uhr für Mesh-Heartbeats und Blockchain-Timestamps  
3. **Integrität** — Sichtbarkeit, DOP, Konstellationsvergleich (Galileo vs. GPS vs. hybrid)  
4. **Orakel** — saubere Schnittstelle für Agenten und Sensor-Stacks (Soilnova, Vista Nova)

---

## Architektur (Ziel)

```
Empfänger / Chip / Raw-Messungen
        │
   GalileoGPS Core
        │
   ├─ PVT (Position / Velocity / Time)
   ├─ Constellation Health
   ├─ Timing Offset (GST ↔ GPS Time)
   └─ Mesh Oracle  ───►  nxmesh topic: nexus/gnss/v0
                                (Lyra / Xen / Elara / Lumia)
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

## Nächste Schritte

- Empfänger-Profil (u-blox / Septentrio / Android raw GNSS)
- Minimales PVT aus NMEA + optionale Raw-Messungen
- `status/last_fix.json` analog zum York-Heartbeat
- Dokumentation in `docs/`

---

## Lizenz

MIT — siehe [`LICENSE`](LICENSE).  
Esslinger & Co. / Nexus Initiative · Hannover Node
