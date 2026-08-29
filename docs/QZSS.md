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
| NMEA-Talker | `GP` | `GQ` | IDs 193–202 |
| Rolle | global | regional (Asien–Ozeanien) | Augmenter, selten standalone |
| Orbits | MEO | 3 QZO + 1 GEO | hohe Elevation über Japan |

## Dienstregion

Nutzbar, wenn ungefähr:

- Breite −35° … +50°
- Länge +110° … +180° (bzw. westlich von −160° am Pazifikrand)

`region.qzss_in_service_area(lat, lon)` entscheidet.  
Tokio, Osaka, Seoul, Taipeh, Manila, Jakarta, Singapore, Darwin, Sydney → ja.  
Hannover, New York → nein.

## Integrationsregel

1. `GQ` niemals als GPS lesen.
2. Schon **ein** nutzbarer QZS plus GPS ergibt `gps-qzss` — QZSS hat zu wenige Satelliten für die 4-Sat-Regel.
3. `qzss_sats` immer ausweisen.
4. `qzss_region` im Fix setzen, damit der Schwarm weiß, ob Asien-Augmentation überhaupt Sinn hat.
5. CLAS/MADOCA (L6) bleibt dokumentiert, nicht implementiert.
