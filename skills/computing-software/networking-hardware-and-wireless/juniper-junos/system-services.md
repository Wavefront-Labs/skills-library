---
id: computing-software.networking-hardware-and-wireless.juniper-junos.system-services
name: system-services
category: computing-software
field: networking-hardware-and-wireless
product: juniper-junos
tags: [juniper-junos, system-services, ssh, netconf-service, management-access]
level: practitioner
status: draft
description: "Enable SSH, NETCONF and other Junos system services and restrict management-plane access."
sources: ["https://www.juniper.net/documentation/", "https://www.juniper.net/documentation/us/en/software/junos/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Enabling system services and securing management
Goal: allow only the management protocols you need, only from known networks.

```
set system services ssh root-login deny
set system services ssh protocol-version v2
set system services ssh max-sessions-per-connection 3
set system services netconf ssh
set system services ssh connection-limit 10
set system services ssh rate-limit 5
delete system services telnet
set system host-name edge1
set system name-server 192.0.2.53
set system domain-name example.net
```

- Reach is controlled in two places: the service must be enabled under `system services`, and on SRX/security platforms the zone `host-inbound-traffic system-services` must allow it. On routers/switches use a loopback filter.
- `set system services web-management https` enables J-Web (disable if unused).

Gotcha: enabling `ssh` alone on an SRX does nothing for a zone that does not list `ssh` under host-inbound-traffic; the connection is silently dropped.

## Verify
- `show system connections | match "\.22 "` shows the listener.
- `ssh` from an allowed host succeeds and from a disallowed one times out.
