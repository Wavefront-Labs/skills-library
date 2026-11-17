---
id: computing-software.systems-network-administration.pi-hole.docker-capabilities
name: docker-capabilities
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-capabilities, net-admin, cap-add]
level: advanced
status: docs-checked
description: "Decide which Linux capabilities the Pi-hole container needs, and when NET_ADMIN, SYS_TIME and SYS_NICE can be skipped."
sources: ["https://docs.pi-hole.net/docker/configuration/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Container capabilities for Pi-hole

FTL expects these capabilities:

| Capability | Why |
| --- | --- |
| `CAP_NET_BIND_SERVICE` | Bind sockets below 1024 (DNS on port 53) |
| `CAP_NET_RAW` | Raw and packet sockets: DHCPv6 and checking an IP is unused before leasing it |
| `CAP_NET_ADMIN` | Modify routing tables; insert neighbor-table entries to answer DHCP with unicast |
| `CAP_SYS_NICE` | Raise FTL's priority when CPU time is scarce |
| `CAP_CHOWN` | Change ownership of logs and databases when started as another user |
| `CAP_SYS_TIME` | Set the system time through NTP |

The image grants those that are available to the FTL process, even when it runs as non-root.

Docker does not include `NET_ADMIN` for non-privileged containers by default, so add it explicitly:

```yaml
cap_add:
  - NET_ADMIN
```

Or with `docker run`: `--cap-add=NET_ADMIN`.

**Can I skip it?** If DHCP and IPv6 Router Advertisements are not in use, `NET_ADMIN` should be safe to omit. `SYS_TIME` is only needed when Pi-hole sets the host clock as an NTP client. A very cautious setup can explicitly drop `NET_RAW` to stop FTL gaining it.

**Checklist**

1. DHCP server in the container: add `NET_ADMIN`.
2. NTP client adjusting host time: add `SYS_TIME`.
3. Otherwise keep the list minimal.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Docker Configuration (docker/configuration). Nothing needed removing.
Method: documentation only; no commands were run.
