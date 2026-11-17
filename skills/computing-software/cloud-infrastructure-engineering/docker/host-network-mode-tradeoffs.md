---
id: computing-software.cloud-infrastructure-engineering.docker.host-network-mode-tradeoffs
name: host-network-mode-tradeoffs
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, host-network-mode, host-networking-tradeoffs, network-mode-host, port-publishing, network-performance, multicast, docker-desktop-host-networking, security]
level: practitioner
status: docs-checked
description: "Decide when --network host is worth it: what you gain (no NAT, port ranges, multicast), what breaks (isolation, -p, DNS names, port clashes), and Desktop/rootless caveats."
sources: ["https://docs.docker.com/engine/network/drivers/host/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/reference/compose-file/services/#network_mode", "https://docs.docker.com/reference/compose-file/services/#ports"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Host network mode: tradeoffs

`--network host` (Compose `network_mode: host`) puts the container in the host's network
namespace. No veth, no bridge, no NAT: the process binds host interfaces directly.

## When it is the right call
- **Large port ranges or dynamic ports**: host mode needs no NAT and no userland-proxy per port (the Docker docs name this and performance as the use cases).
- **Performance-sensitive services**: measure first; for most HTTP services the difference is small.

## What you give up
- **Isolation**: the container's network stack is not isolated from the Docker host (it shares the host's network namespace and gets no IP of its own). Treat it as a privilege; storage, process and user namespaces stay isolated.
- **`-p` is ignored** (`WARNING: Published ports are discarded when using host network mode`).
  Port conflicts with host processes and other host-mode containers are now your problem.
- **Scaling**: two replicas of the same service clash on the same port.
- Docker creates no firewall rules for host networking, so the host firewall applies as for any host process (published bridge ports, by contrast, bypass ufw).

## Platform caveats
- **Docker Desktop**: supported from 4.34 as an opt-in (Settings → Resources → Network → Enable host networking). It works at layer 4 only (protocols below TCP/UDP are not supported), containers cannot bind to the host's IP addresses, it does not work with Enhanced Container Isolation, and only Linux containers are supported.
- **Swarm**: a service can use `docker service create --network host`; control traffic still uses an overlay, and only one task per node can bind a given port.

## Safer middle grounds
- Need LAN presence? macvlan/ipvlan give the container its own LAN IP while
  keeping it out of the host namespace.

## Compose
```yaml
services:
  mdns:
    image: example/mdns-repeater
    network_mode: host
    # ports: are invalid alongside network_mode: host
```

## Verify
```bash
docker run --rm --network host alpine ip addr        # shows host interfaces
docker run -d --network host --name web nginx && ss -ltnp | grep ':80 '   # nginx on host port 80
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the host driver page (use cases, no IP, `-p` ignored with the exact warning, Docker Desktop 4.34+ opt-in, Desktop limitations, Swarm `--network host`), the packet-filtering page (no firewall rules for host/macvlan/ipvlan) and the Compose reference (ports not allowed with `network_mode: host`). Removed unconfirmed claims: multicast/mDNS and tooling use cases, metadata-endpoint reach, DNS/embedded-DNS behaviour, rootless host-mode details, and source-IP statements.

Method: documentation only; no commands were run.
