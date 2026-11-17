---
id: computing-software.cloud-infrastructure-engineering.docker.attachable-and-encrypted-overlay-networks
name: attachable-and-encrypted-overlay-networks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, overlay-network, overlay-encrypted, attachable-overlay, attachable, swarm-overlay, swarm-ports, vxlan-4789, overlay-encryption, swarm]
level: advanced
description: "Create attachable overlays so standalone containers join Swarm networks, enable IPsec encryption with --opt encrypted, and open the Swarm ports (2377, 7946, 4789) correctly."
sources: ["https://docs.docker.com/engine/network/drivers/overlay/", "https://docs.docker.com/engine/swarm/networking/", "https://docs.docker.com/engine/swarm/swarm-tutorial/#open-protocols-and-ports-between-the-hosts", "https://docs.docker.com/reference/cli/docker/swarm/init/#data-path-port"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Attachable and encrypted overlay networks

## Ports between Swarm nodes
| Port | Proto | Purpose |
|---|---|---|
| 2377 | TCP | Swarm control plane (default; configurable with `docker swarm join --listen-addr`) |
| 7946 | TCP + UDP | communication among nodes (not configurable) |
| 4789 | UDP | VXLAN overlay data (default; configurable only at init: `docker swarm init --data-path-port`, range 1024-49151) |
| ESP (IP protocol 50) | - | only needed for encrypted overlays (`--opt encrypted`) |
If UDP 4789 is already in use in your environment, pick another data path port when the swarm is initialised.

## Attachable overlays
```sh
docker network create -d overlay --attachable --subnet 10.30.0.0/24 shared
docker run -d --name debug --network shared nicolaka/netshoot sleep infinity   # standalone container on a swarm network
```
- Without `--attachable`, only services can use the overlay.
- Uses: one-off admin/migration or debugging containers that talk to services.
- The Docker host must be part of a swarm, even to connect standalone containers.

## Encryption
```sh
docker network create -d overlay --opt encrypted --attachable secure-net
```
```yaml
networks:
  backend:
    driver: overlay
    driver_opts: { encrypted: "true" }
```
- Enables IPsec encryption at the level of the VXLAN. It has a non-negligible performance penalty, so test before production.
- Swarm management and control-plane data is always encrypted; application data is not encrypted by default, so only **data** traffic needs this option.
- If encapsulation overhead causes fragmentation, lower the network MTU with
  `--opt com.docker.network.driver.mtu=<n>`, choosing `<n>` from a measured path MTU.
- Overlay encryption is not supported on Windows: do not attach Windows containers to an encrypted overlay
  (they cannot talk to Linux containers on it and their data traffic is not encrypted). Firewalls must permit ESP.

## Gotchas
- Set `--subnet` explicitly (or the swarm's `--default-addr-pool` at init) to avoid overlaps with existing ranges.
- Overlay networks can become unstable when about 1000 containers are co-located on one host (documented kernel limitation).

## Verify
```sh
docker network inspect secure-net -f '{{json .Options}}'   # the encrypted option is listed
sudo tcpdump -ni eth0 esp                                   # ESP packets between nodes
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the overlay driver page, the Swarm networking guide, the Swarm tutorial port list and the `swarm init` reference: ports 2377/7946/4789 and their configurability, ESP for encrypted overlays, `--attachable`, `--opt encrypted` (IPsec at VXLAN level, performance penalty), control-plane always encrypted, Windows limitation, the 1000-container limit. Removed unconfirmed claims: AES-GCM mode, 12-hour key rotation, specific MTU byte figures, cloud/VMware port clashes, same-node and worker-inspect gotchas, `ip xfrm` output.

Method: documentation only; no commands were run.
