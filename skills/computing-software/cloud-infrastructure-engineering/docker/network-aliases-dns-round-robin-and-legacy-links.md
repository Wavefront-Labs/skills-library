---
id: computing-software.cloud-infrastructure-engineering.docker.network-aliases-dns-round-robin-and-legacy-links
name: network-aliases-dns-round-robin-and-legacy-links
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, embedded-dns, service-discovery, network-alias, compose-aliases, dns-round-robin, legacy-links, link-flag, default-bridge]
level: practitioner
description: "Give containers extra DNS names with --network-alias and Compose aliases, load-spread with shared aliases, and replace legacy --link and default-bridge setups."
sources: ["https://docs.docker.com/engine/network/#dns-services", "https://docs.docker.com/reference/cli/docker/container/run/#network-alias", "https://docs.docker.com/reference/compose-file/services/#aliases", "https://docs.docker.com/engine/network/links/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Network aliases, DNS round robin and legacy links

## Names a container answers to (user-defined networks)
- its `--name`,
- each `--network-alias` on that network,
- in Compose: the **service name**, plus `aliases:`.

```sh
docker network create appnet
docker run -d --name web1 --network appnet --network-alias db --network-alias web nginx
docker run --rm --network appnet alpine nslookup db
```
Compose:
```yaml
services:
  pg:
    image: postgres
    networks:
      backend:
        aliases: [db, pg.internal]
```
Aliases are **per network**: a container on two networks can be `db` on one and nothing on
the other. Rename a dependency without touching clients by aliasing the new container.

## DNS round robin
Several containers with the same alias -> the embedded DNS returns all their IPs:
```sh
docker run -d --network appnet --network-alias search nginx   # x3
docker run --rm --network appnet alpine nslookup search    # 3 A records
```
Compose `--scale api=3` does the same with the service name. Limits:
- It's DNS, not load balancing: clients that cache the first IP stick to one backend.
- Swarm services use a virtual IP by default; DNS round robin (`dnsrr`) is configurable per service.

## Default bridge and --link (legacy)
On the default `bridge` network there is **no name resolution**. `--link` used to inject
`/etc/hosts` entries and env vars (`DB_PORT_5432_TCP_ADDR`):
```sh
docker run -d --name db postgres
docker run --link db:database app:1            # legacy - don't
```
Status: links on the default `bridge` network are deprecated (Docker emits a warning from Engine 29.6; removal is scheduled for Engine 30.0), and the legacy link environment variables were deprecated in Engine 28.4. Links on non-default networks remain supported.
Migration: create a user-defined network, attach both, use names/aliases.

## Gotchas
- Aliases resolve through the embedded DNS inside the network; they don't resolve from the host, so use published ports from there.

## Verify
`docker run --rm --network appnet alpine getent hosts db` returns the IP(s);
`docker inspect -f '{{json .NetworkSettings.Networks.appnet.Aliases}}' pg-16` lists aliases.

## Checked

Docker Engine 29.x documentation (docker/docs main, which lists Engine 29.8 as current), checked 2026-10-24. Confirmed against the legacy links page (default-bridge deprecation from 29.6 with removal in 30.0, env-var deprecation in 28.4, non-default networks still supported, `/etc/hosts` entries), the bridge driver page (name or alias resolution on user-defined networks), the `docker run`/`network connect` references (`--network-alias`, `--alias`), the Compose reference (`aliases`) and the Swarm networking guide (VIP default, `dnsrr`). Removed pinned image tags, Nginx/JVM resolver advice, the short-ID and hostname claims, and the `links:` migration remark.

Method: documentation only; no commands were run.
