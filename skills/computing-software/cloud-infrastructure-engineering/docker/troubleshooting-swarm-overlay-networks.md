---
id: computing-software.cloud-infrastructure-engineering.docker.troubleshooting-swarm-overlay-networks
name: troubleshooting-swarm-overlay-networks
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, swarm-overlay, overlay-troubleshooting, port-7946, vxlan-4789, data-path-port, mtu-mismatch]
level: advanced
status: docs-checked
description: "Fix cross-node Swarm traffic: ports 2377/7946/4789 and ESP, VXLAN port clashes (--data-path-port), MTU overhead, NIC checksum offload bugs, stale VIPs, inspect -v."
sources: ["https://docs.docker.com/engine/swarm/networking/", "https://docs.docker.com/engine/network/drivers/overlay/", "https://docs.docker.com/reference/cli/docker/swarm/init/#data-path-port", "https://docs.docker.com/reference/cli/docker/network/inspect/#verbose"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Troubleshooting Swarm overlay networks

Symptom pattern: services on the **same** node talk fine; across nodes, DNS resolves the
service VIP but connections hang or reset.

## 1. Ports between all nodes
| Port | Purpose |
|---|---|
| TCP 2377 | Swarm control plane (default; `docker swarm join --listen-addr`) |
| TCP + UDP 7946 | Communication among nodes (not configurable) |
| UDP 4789 | VXLAN data plane (default; `--data-path-port`) |
| IP protocol 50 (ESP) | Encrypted overlays (`--opt encrypted`) |

```bash
nc -zv <other-node> 2377; nc -zvu <other-node> 7946; nc -zvu <other-node> 4789   # UDP checks are indicative only
sudo tcpdump -ni eth0 udp port 4789     # should show traffic when containers on 2 nodes talk
```
Check that security groups and host firewalls allow the UDP ports as well as TCP.

## 2. VXLAN port conflicts
If another service already uses UDP 4789, initialise the swarm with another port (1024-49151):
`docker swarm init --data-path-port 4790`. The data path port can only be set when the swarm is initialised and applies to all nodes that join.

## 3. MTU
VXLAN encapsulation adds overhead, so an underlay MTU close to 1500 can leave too little room for overlay packets (small pings work, large packets vanish).
```bash
docker network create -d overlay --opt com.docker.network.driver.mtu=1400 --attachable app-net
```
The ingress network needs the same treatment (recreate ingress with the MTU option).

## 4. Inspect the overlay state
```bash
docker network inspect -v app-net      # Peers (nodes with a task attached) and service VIPs/tasks
```
Missing peers suggests the node-to-node ports (7946) are blocked.

## 5. Advertise address
Nodes with several NICs must advertise the reachable one:
`docker swarm join --advertise-addr <ip> --data-path-addr <ip> ...`; a wrong address shows up
as peers using a private/unreachable IP in `network inspect -v`.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the overlay driver and Swarm networking pages (ports, ESP, `--data-path-port` range and init-only rule, ingress network recreation with `com.docker.network.driver.mtu`, `--advertise-addr`/`--data-path-addr`) and the `network inspect` reference (`--verbose` for Swarm overlay networks, Peers). Removed unconfirmed claims: the 50-byte figure, VMware NSX port clash, checksum-offload workaround, netns/nsenter inspection, `service update --force` for stale endpoints, and the `jq` pipeline.

Method: documentation only; no commands were run.
