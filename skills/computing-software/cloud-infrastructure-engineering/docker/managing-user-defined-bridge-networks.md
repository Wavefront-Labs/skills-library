---
id: computing-software.cloud-infrastructure-engineering.docker.managing-user-defined-bridge-networks
name: managing-user-defined-bridge-networks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-defined-network, custom-network, subnet-flag, ip-range, gateway-flag, static-ip, ipv4-address, network-connect, network-disconnect, multi-network, network-priority, gw-priority, network-inspect]
level: practitioner
description: "Create bridge networks with explicit subnet, gateway and ip-range, give containers static IPs, attach and detach live, and control the default route with gw-priority."
sources: ["https://docs.docker.com/reference/cli/docker/network/create/", "https://docs.docker.com/reference/cli/docker/network/connect/", "https://docs.docker.com/engine/network/#connecting-to-multiple-networks", "https://docs.docker.com/reference/compose-file/services/#ipv4_address-ipv6_address", "https://docs.docker.com/reference/compose-file/services/#gw_priority"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Managing user-defined bridge networks

## Create with explicit addressing
```sh
docker network create \
  --driver bridge \
  --subnet 172.30.10.0/24 \
  --gateway 172.30.10.1 \
  --ip-range 172.30.10.128/25 \
  --label env=prod --label owner=platform \
  appnet
```
- `--ip-range` restricts **automatic** allocation to a sub-range, leaving the rest free for
  static assignments - avoids collisions between static and dynamic IPs.
- Choose subnets that don't overlap office/VPN/cloud ranges (or set `default-address-pools`).

## Static IPs
```sh
docker run -d --name dns --network appnet --ip 172.30.10.10 coredns/coredns
```
```yaml
services:
  dns:
    networks:
      appnet: { ipv4_address: 172.30.10.10 }
networks:
  appnet:
    ipam:
      config: [{ subnet: 172.30.10.0/24, ip_range: 172.30.10.128/25, gateway: 172.30.10.1 }]
```
Only on user-defined networks with a user-specified subnet. Prefer names; use static IPs
for things referenced by IP (DNS servers, legacy allowlists).

## Connect, disconnect
```sh
docker network connect --alias cache --ip 172.30.10.20 appnet redis
docker network disconnect appnet redis
docker network disconnect -f appnet ghost     # remove stale endpoint of a deleted container
```
Live: no restart needed.

## Multiple networks and the default route
A container on several networks gets one interface per network; the **default gateway**
comes from one of them. Since Engine 28, choose explicitly:
```sh
docker run --network name=frontnet,gw-priority=1 --network backnet app:1
docker network connect --gw-priority 1 frontnet app
```
The highest priority provides the default gateway (default `0`; positive and negative values are accepted). The option arrived with Engine 28.0 (API 1.48); if priorities are equal, endpoints are sorted lexicographically by network name and the first wins.
Compose: `networks: { frontnet: { gw_priority: 1 } }` (the Compose `priority` key only orders connection and does not affect the gateway).

## Inspect
```sh
docker network inspect appnet -f '{{json .IPAM.Config}}'
docker network inspect appnet -f '{{range .Containers}}{{.Name}} {{.IPv4Address}}{{println}}{{end}}'
docker network ls --filter label=env=prod
docker network rm appnet                       # fails while endpoints exist
```

## Verify
`docker exec app ip route` shows the expected default via; `docker network inspect` lists
containers with the intended IPs.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed `--subnet`, `--gateway`, `--ip-range`, `--label` (network create reference), `--alias`, `--ip`, `--gw-priority` (network connect reference), the multi-network and `gw-priority` text in the networking overview, the `GwPriority` entry (API 1.48, Engine 28.0, lexicographic tie-break) in the Engine API changelog, and the Compose `gw_priority` and `priority` entries. Removed the claim about the pre-28 gateway selection and the loopback-only remark.

Method: documentation only; no commands were run.
