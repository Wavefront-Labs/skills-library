---
id: computing-software.cybersecurity-defensive.palo-alto-pan-os.pan-os-virtual-systems
name: pan-os-virtual-systems
category: computing-software
field: cybersecurity-defensive
product: palo-alto-pan-os
tags: [virtual-systems, pan-os, vsys, multi-tenancy, inter-vsys, external-zone, vsys-admin]
level: practitioner
status: draft
description: "Create PAN-OS virtual systems for tenant or business unit separation, with inter-vsys routing through external zones and role scoping."
sources: ["https://docs.paloaltonetworks.com/pan-os/11-1/pan-os-admin/virtual-systems"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
Goal: multiple logical firewalls on one platform with separate policy, objects and administrators.

```
configure
set deviceconfig setting management multi-vsys on
set vsys vsys2 display-name tenant-b
set vsys vsys2 import network interface [ ethernet1/5 ethernet1/6 ]
set vsys vsys2 import network virtual-router default
set vsys vsys2 zone tenant-b-trust network layer3 ethernet1/5
set vsys vsys2 zone tenant-b-untrust network layer3 ethernet1/6
commit
```
Each vsys has its own zones, rulebases, objects and (optionally) a visible-virtual-system list for inter-vsys traffic. Inter-vsys traffic uses `external` zones and the traffic crosses the dataplane twice, consuming resources.

Per-vsys admins use `vsysadmin` roles scoped to that vsys. Resources (sessions, rules, VPN tunnels) can be capped by a Resource profile.

Gotchas
- Multi-vsys capability needs a supported model and may require a licence or reboot (confirm).
- Shared gateway design (several vsys sharing one untrust interface) needs a shared gateway object and careful NAT.
- Logs are tagged by vsys; ensure log forwarding and report filters use it.

## Verify
```
show system info | match multi-vsys
show running resource-monitor
```
Traffic between zones in different vsys appears in both vsys traffic logs.
