---
id: computing-software.networking-hardware-and-wireless.juniper-junos.jti-telemetry
name: jti-telemetry
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, telemetry, jti, gnmi, streaming-telemetry]
level: practitioner
status: draft
description: "Stream Junos interface and routing data via JTI or gNMI to a collector."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Junos streaming telemetry (JTI and gNMI)
Goal: push counters instead of polling SNMP.

```
set services analytics streaming-server COLLECTOR remote-address 192.0.2.80
set services analytics streaming-server COLLECTOR remote-port 50051
set services analytics export-profile EP local-address 10.255.0.1
set services analytics export-profile EP reporting-rate 30
set services analytics export-profile EP format gpb
set services analytics export-profile EP transport udp
set services analytics sensor IFD server-name COLLECTOR export-name EP resource /junos/system/linecard/interface/
```

```
set system services extension-service request-response grpc clear-text port 32767
```

- Native (JTI) uses UDP or gRPC dial-out/in; OpenConfig gNMI is available on newer releases and platforms: confirm support and paths.
- Collectors like Telegraf or gnmic subscribe with a sample interval.
- Use TLS (`ssl`) for anything beyond a lab; clear-text is for testing only.

Gotcha: sensor paths are platform-specific (`/junos/system/linecard/...` differ on QFX vs MX). Use the Juniper Telemetry Explorer for your release.

## Verify
- `show agent sensors` lists the sensor active, and the collector receives messages.
