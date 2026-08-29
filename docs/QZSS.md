# QZSS-Integration (Asien)

QZSS (Michibiki) ist das regionale japanische System. In GalileoGPS ist es kein globaler Pflichtkern wie GPS oder Galileo, sondern der **Asien-Augmenter**: gleiche Zeitskala wie GPS, QZS-Orbits fast im Zenit über Japan, nutzbar von Ostasien bis Ozeanien.

## Warum QZSS extra zählt

- Über Tokio, Seoul, Taipei, Manila, Sydney steht mindestens ein QZS oft sehr hoch — genau dort, wo Straßenschluchten GPS ausblenden.
- Signale L1 C/A / L1C / L5 sind GPS-kompatibel; L6 trägt CLAS / MADOCA (cm-Klasse, eigener Decoder, nicht in v0.4).
- Hannover sieht QZSS praktisch nicht. Der Parser zählt trotzdem, das Orakel markiert `qzss_region=false`.

## Systemunterschiede

| Thema | GPS | QZSS | Brücke |
|---|---|---|---|
| Zeit | GPST = UTC + 18 s | QZSST ≡ GPST | `timebase.qzss_to_utc` = `gps_to_utc` |
| Koordinaten | WGS84 | JGD2011 / ITRF | Meter-Äquivalenz, Ausgabe WGS84 |
| NMEA-Talker | `GP` | `GQ` | IDs 193–199 |
| Rolle | global | regional (Asien–Ozeanien) | Augmenter, selten standalone |
| Orbits | MEO | QZO + GEO + QGEO | hohe Elevation über Japan |

## QZS-4 / QZS-5

Beide Slots sind QZO (*a* = 42 165 km, *e* = 0,075, *i* = 41°, *ω* = 270°).

- **QZS-4** — aktiv, PRN 195, Zentrum **137,5° E**, Ω = 347°
- **QZS-5** — verloren (H3 F8, 2025-12-22), Soll-Zentrum **139° E**, Ω = 126°

Vollständige Elemente: [`docs/QZSS_ORBITS.md`](QZSS_ORBITS.md) · Code: `galileogps.qzss_orbits`

## Dienstregion

Nutzbar, wenn ungefähr Breite −45° … +50° und Länge +95° … +180° (bzw. westlich von −160°).

`region.qzss_in_service_area(lat, lon)` entscheidet. Tokio, Seoul, Singapore, Sydney → ja. Hannover → nein.

## Integrationsregel

1. `GQ` niemals als GPS lesen.
2. Schon **ein** nutzbarer QZS plus GPS ergibt `gps-qzss`.
3. `qzss_sats` immer ausweisen.
4. `qzss_region` im Fix setzen.
5. CLAS/MADOCA (L6) bleibt dokumentiert, nicht implementiert.
