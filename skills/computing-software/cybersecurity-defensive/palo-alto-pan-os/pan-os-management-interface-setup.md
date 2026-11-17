---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-management-interface-setup
name: pan-os-management-interface-setup
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [management-interface, pan-os, mgmt-port, deviceconfig, initial-setup, dns, ntp]
level: practitioner
status: draft
description: "Set the PAN-OS management IP, DNS, NTP and permitted services from the CLI, then lock the management plane to trusted sources."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/firewall-administration/management-interfaces"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: bring a new firewall or Panorama to a reachable, time-synced, hardened management plane before anything else is configured.

```
configure
set deviceconfig system ip-address 192.0.2.10 netmask 255.255.255.0 default-gateway 192.0.2.1
set deviceconfig system dns-setting servers primary 192.0.2.53 secondary 192.0.2.54
set deviceconfig system ntp-servers primary-ntp-server ntp-server-address 192.0.2.123
set deviceconfig system hostname fw-edge-01
set deviceconfig system service disable-telnet yes disable-http yes
set deviceconfig system permitted-ip 192.0.2.0/28
commit
```

Notes
- `permitted-ip` is an allow list for the management plane; once committed, any host outside it loses SSH and HTTPS. Include the address you are connected from.
- Use an interface management profile (Network > Network Profiles) for management services on data-plane interfaces; do not expose the dedicated management port to the internet.
- A service route is needed when DNS, updates or syslog should leave via a data-plane interface rather than the management port: Device > Setup > Services > Service Route Configuration.

Gotchas
- The dedicated management port has its own default gateway; it does not use the virtual router. Updates that fail with "no route" are usually a missing service route (confirm in your version).
- Changing the management IP over the same session drops you; commit from the console if unsure.

## Verify
```
show system info | match ip-address
show interface management
ping source 192.0.2.10 host 192.0.2.53
show ntp
```
Expect `show ntp` to list the server as synched.
