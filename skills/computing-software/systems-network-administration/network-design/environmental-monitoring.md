---
id: computing-software.systems-network-administration.network-design.environmental-monitoring
name: environmental-monitoring
category: computing-software
field: systems-network-administration
product: network-design
tags: [network-design, monitoring, environmental-monitoring, temperature-sensors, ups-monitoring, water-leak]
level: practitioner
status: draft
description: "Monitor the physical environment of network rooms: temperature and humidity at rack inlets, UPS/PDU status, water leak, door and smoke sensors, with sensible alert thresholds."
sources:
  - https://www.ashrae.org/technical-resources/bookstore/datacom-series
  - https://www.apc.com/us/en/product-range/61822-netbotz/
  - https://networkupstools.org/docs/user-manual.chunked/index.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Environmental monitoring

## Sensors
| Sensor | Placement | Alert |
|---|---|---|
| Temperature | rack **front inlet**, top/middle/bottom in hot racks; IDF room | warn 27 C, critical 32 C inlet (ASHRAE recommended 18-27 C) |
| Humidity / dew point | room | outside 20-80 % RH or dew point -9 to 15 C (ASHRAE) |
| Water leak (rope) | under raised floor, near AC units and pipes | any |
| Door contact / camera | rack and room doors | outside hours |
| Smoke / VESDA | room | via fire system and NOC |
| Power | UPS on battery, runtime remaining, PDU load per phase | on battery, < 15 min runtime, > 80 % load |

## Data sources
- Switch and router internal temperature sensors via SNMP (ENTITY-SENSOR-MIB, CISCO-ENVMON-MIB)
  or `show environment`: cheap coverage for every IDF, though internal temps run hotter than inlet.
- Dedicated probes (NetBotz, AKCP, Geist) for inlet temperature and leak/door.
- UPS via SNMP card or NUT (`upsc ups@host`), PDUs via SNMP.

## Alerting
- Rate-of-rise alerts catch AC failure early (e.g. +3 C in 10 min).
- Notify facilities as well as network on-call; define who drives to the site.
- Automated graceful shutdown scripts on long power outages (NUT `upsmon`).

## Verify
- [ ] Every IDF/MDF reports temperature; UPS on-battery test raises an alert end to end; leak sensor test triggers.
