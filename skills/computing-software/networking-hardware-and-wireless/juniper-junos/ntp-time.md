---
id: computing-software.networking-hardware-and-wireless.juniper-junos.ntp-time
name: ntp-time
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, ntp, time-sync, timezone, ntp-boot-server]
level: practitioner
status: draft
description: "Configure NTP servers, time zone and boot-server on Junos, and check synchronisation."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NTP and time
Goal: accurate time so logs, certificates and commits line up.

```
set system time-zone UTC
set system ntp boot-server 192.0.2.10
set system ntp server 192.0.2.10 prefer
set system ntp server 192.0.2.11
set system ntp source-address 10.255.0.1
```

```
user@host> show ntp associations
user@host> show ntp status
user@host> set date ntp 192.0.2.10
user@host> show system uptime
```

- `boot-server` sets the clock during boot, before normal NTP; without it large offsets will not correct.
- On management-VRF designs, NTP must be reachable through the right routing instance (confirm on your release for `routing-instance`).

Gotcha: NTP refuses to sync when the offset is large (over about 128 ms steps are limited) and in `show ntp associations` the peer sits at `reach 0`. Fix with `set date ntp` once, then let NTP slew.

Operational tip: use at least three NTP servers for a majority vote, and monitor offset on the NMS so drift is caught before certificate or log-correlation problems appear.

## Verify
- `show ntp associations` shows `*` next to the selected peer with `reach 377`.
