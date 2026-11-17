---
id: computing-software.cloud-infrastructure-engineering.docker.user-defined-networks-and-isolation
name: user-defined-networks-and-isolation
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, user-defined-network, network-isolation, custom-network, bridge, internal-network, network-segmentation, icc, docker-network-create, subnet, aliases, compose-networks, default-bridge]
level: practitioner
status: docs-checked
description: "Designing container networks for isolation: why user-defined bridges beat the default bridge, --internal networks for DB tiers, multi-homed proxies, subnet/gateway options, aliases, and icc=false."
sources: ["https://docs.docker.com/engine/network/drivers/bridge/", "https://docs.docker.com/reference/cli/docker/network/create/", "https://docs.docker.com/engine/network/", "https://docs.docker.com/reference/compose-file/networks/", "https://docs.docker.com/engine/network/packet-filtering-firewalls/", "https://docs.docker.com/reference/compose-file/services/#gw_priority"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# User-defined networks and isolation

**Goal:** containers can only talk to the containers they need, a compromised web tier
cannot reach the database of another project, and names resolve without `--link`.

## Default bridge vs user-defined bridge
| | `bridge` (docker0, default) | `docker network create mynet` |
|---|---|---|
| Name resolution | none (legacy `--link` only) | embedded DNS at 127.0.0.11, by container name and alias |
| Isolation | every container on the host shares it | only members talk; separate networks are firewalled from each other |
| Connect/disconnect live | no | `docker network connect/disconnect` while running |
| `icc` | one global switch | per network via driver option |

Rule: never deploy on the default bridge. Compose already creates `<project>_default` per
project, which is why Compose projects can't see each other by name.

## Create with the options that matter
```bash
docker network create \
  --driver bridge \
  --subnet 10.10.0.0/24 --gateway 10.10.0.1 \
  --ip-range 10.10.0.128/25 \
  -o com.docker.network.bridge.name=br-app \
  -o com.docker.network.bridge.enable_icc=true \
  -o com.docker.network.bridge.enable_ip_masquerade=true \
  app-net
docker run -d --name api --network app-net --network-alias backend --ip 10.10.0.10 api:1
```
- Explicit `--subnet` only when something external (firewall rules, a VPN) needs to know the
  range; otherwise let Docker pick from `default-address-pools` in `daemon.json`
  (`{"default-address-pools":[{"base":"10.200.0.0/16","size":24}]}` avoids collisions with
  `172.17.0.0/16`-style corporate ranges).
- `--ip` needs a `--subnet`; static IPs are rarely worth it, use names.
- `-o com.docker.network.bridge.name` gives a predictable interface name for host firewall
  rules and tcpdump.
- `--network-alias` lets several containers answer the same name (poor man's round-robin
  via DNS) and is what Compose `aliases:` sets.

## Isolation patterns
**Internal (no egress) tier:**
```bash
docker network create --internal db-net
```
`--internal` restricts external access to the network: a DB on `db-net` should be unreachable from outside and unable to phone home.

**Multi-homed service as the only bridge between tiers:**
```yaml
services:
  proxy: {networks: [frontend, backend], ports: ["443:443"]}
  api:   {networks: [backend]}
  db:    {networks: [backend]}
networks:
  frontend: {}
  backend: {internal: true}
```
`proxy` reaches the internet and `api`; `db` is reachable only from `backend` members.
`docker run` accepts several `--network` flags, and `docker network connect` adds networks to a running container; Compose handles multi-network natively.

**Disable container-to-container chatter on one network:**
`-o com.docker.network.bridge.enable_icc=false` disables inter-container connectivity on that network.
`"icc": false` in `daemon.json` applies only to the default bridge.

**Published ports are host-wide.** A container on an isolated network that does `-p 5432:5432`
is reachable from the LAN regardless of the network design; bind to loopback `-p
127.0.0.1:5432:5432` or don't publish. Also note `DOCKER-USER` chain rules are needed to
block external hosts, since Docker's published-port rules precede the `INPUT` chain
(see `iptables` skill).

## Cross-project / existing networks
```yaml
networks:
  shared:
    external: true      # must already exist; Compose will not create or delete it
    name: platform-net
```
`docker network create platform-net` once, then every Compose project that needs the shared
reverse proxy joins it. Containers find each other by service name across projects only on
the shared network; aliases are per-network.

## Limits and gotchas
- A container can be on many networks; Docker chooses the default gateway and may change it when connections change. Set `gw-priority` (Engine 28.0+; `docker run --network name=n,gw-priority=1`) or Compose `gw_priority` to pin it. The Compose `priority` key does not affect the gateway.
- A bridge network becomes unstable when about 1000 or more containers connect to it.
- `docker network prune` removes unused user networks; Compose `down` removes its own.
- Removing a network with attached containers fails: `docker network inspect -f
  '{{range .Containers}}{{.Name}} {{end}}' net` to find them.

## Verify
```bash
docker run --rm --network db-net alpine ping -c1 -W1 1.1.1.1          # fails on internal
docker run --rm --network app-net alpine nslookup backend              # resolves the alias
docker run --rm --network frontend alpine nc -zv db 5432               # must fail (different net)
```

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the bridge page (default vs user-defined bridges, options, 1000-container limit), the networking overview (multiple `--network` flags, `gw-priority`, `--internal`), the Compose reference (`gw_priority`; `priority` does not affect the gateway), the `dockerd` reference (`icc` is for the default bridge) and the packet-filtering page (DOCKER-USER, ports published host-wide). Corrected two wrong claims: `docker run` can join several networks at start, and Compose `priority` does not choose the default route. Removed the no-default-route and chain-name claims.

Method: documentation only; no commands were run.
