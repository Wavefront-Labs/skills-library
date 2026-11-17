---
id: computing-software.systems-network-administration.pi-hole.docker-dhcp-network-modes
name: docker-dhcp-network-modes
category: computing-software
field: systems-network-administration
product: pi-hole
tags: [docker-dhcp, macvlan, dhcp-relay]
level: advanced
status: docs-checked
description: "Serve DHCP from a Pi-hole container by choosing host networking, macvlan or a bridge with a DHCP relay."
sources: ["https://docs.pi-hole.net/docker/DHCP/", "https://docs.pi-hole.net/docker/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# DHCP and Docker network modes

Docker's default bridge network isolates the container. DHCP uses broadcasts, which cannot cross from the bridge to your LAN, so a forwarded port 67 alone does not work. Three approaches work.

**Host networking: simple and fast**

The container sits on the LAN like a normal host and shares the host's IP, so port conflicts remain possible. In compose, remove the ports and add:

```yaml
network_mode: host
```

With `docker run` use `--net=host`.

**Macvlan: for NAS devices or hard port conflicts**

The container takes its own new IP from your LAN. This avoids the broadcast problem and port clashes, for example with a NAS web interface. It needs more network knowledge to set up.

**Bridge with a DHCP relay: works well with reverse proxies such as Nginx or Traefik**

A relay forwards the broadcast to the container's published port 67 on the Docker host. Some advanced routers support DHCP relay; otherwise run a software relay on the LAN such as dnsmasq author's DHCP-helper.

Avoid Docker's built-in default bridge. A compose project creates its own network, which is simplest. DHCP in a container also needs `NET_ADMIN`.

**Checklist**

1. Pick host, macvlan or bridge plus relay.
2. Publish `67:67/udp` for the bridge case.
3. Add `NET_ADMIN`.
4. Turn off DHCP on the router first.

## Checked

2026-11-04. Confirmed against the official Pi-hole documentation: Docker DHCP and Network Modes (docker/DHCP); Docker (docker). Nothing needed removing. The DHCP page is dated 2021 while the quick start is newer; no contradiction found.
Method: documentation only; no commands were run.
