---
id: computing-software.firmware-embedded-development.iot-protocols.nb-iot-lte-m-psm
name: nb-iot-lte-m-psm
category: computing-software
field: firmware-embedded-development
product: iot-protocols
tags: [nb-iot-lte-m-psm, iot-low-power-links, nb-iot, lte-m, psm, edrx, iot-protocols]
level: practitioner
status: draft
description: "NB-IoT and LTE-M power saving: Configure cellular IoT for years of battery life."
sources:
  - https://www.gsma.com/solutions-and-impact/technologies/internet-of-things/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NB-IoT and LTE-M power saving

**Goal:** Configure cellular IoT for years of battery life.

## Steps
1. PSM (Power Saving Mode): timers T3324 (active time after TX) and T3412 (periodic TAU, up to 413 days) via AT+CPSMS
2. eDRX: AT+CEDRXS with cycle lengths up to ~43 min (LTE-M) and ~175 min (NB-IoT)
3. Modem is unreachable during PSM, so use device-initiated uploads and LwM2M queue mode
4. Keep payloads tiny and use UDP/CoAP or MQTT-SN to avoid TLS handshake cost (use DTLS Connection ID or TLS session resumption)
5. Network may grant different values than requested; read +CEREG

## Gotcha
Network-granted timers often differ from requested; read back the values and design for them.

## Verify
- [ ] AT+CPSMS? shows granted timers
- [ ] Current profile measured in uA
- [ ] Downlink latency matches eDRX cycle
