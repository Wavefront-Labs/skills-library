---
id: computing-software.cloud-infrastructure-engineering.docker.compose-external-networks-volumes-and-driver-opts
name: compose-external-networks-volumes-and-driver-opts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, compose-networks, compose-volumes, external-network, compose-external, external-volume, compose-network-driver, driver-opts, ipam]
level: practitioner
status: docs-checked
description: "Share networks and volumes across Compose projects with external: true and fixed names, and configure network driver, driver_opts, IPAM and internal networks."
sources: ["https://docs.docker.com/reference/compose-file/networks/", "https://docs.docker.com/reference/compose-file/volumes/", "https://docs.docker.com/compose/how-tos/networking/", "https://docs.docker.com/engine/network/drivers/bridge/", "https://docs.docker.com/engine/network/drivers/macvlan/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---
# Compose external networks, volumes and driver options

## Naming: why projects don't share by default
Compose names the project's own resources with the project name: the network `default` in
project `shop` becomes `shop_default`, and a volume `data` is created as
`<project_name>_data`. A resource with `name:` is used as is and is not scoped with the
project name; an `external` resource is looked up by that name.

## External networks (shared reverse proxy pattern)
```sh
docker network create proxy
```
```yaml
# in each app project
services:
  web:
    networks: [default, proxy]
networks:
  proxy:
    external: true          # must exist; compose won't create or delete it
```
Compose does not try to create an external network and returns an error if it does not
exist. For an external resource every attribute other than `name` is irrelevant, and
Compose rejects a file that sets any other attribute. To share a network without making it
external, declare `name: proxy` in one "owner" project and mark it `external` in the others.

## External / fixed-name volumes
```yaml
volumes:
  pgdata:
    external: true                 # created out of band: docker volume create pgdata
  uploads:
    name: shop-uploads             # fixed name, still managed (created) by compose
```
- `docker compose down` never removes networks and volumes defined as external (Compose
  CLI reference), so `down -v` leaves them alone.
- `name:` keeps the resource name stable when the project name changes (the project name
  defaults to the directory name), so a directory rename does not orphan the old volume.

## Network driver and options
```yaml
networks:
  backend:
    driver: bridge
    internal: true                      # externally isolated network
    driver_opts:
      com.docker.network.bridge.name: br-backend
      com.docker.network.driver.mtu: "1450"
      com.docker.network.bridge.enable_icc: "true"
    ipam:
      config:
        - subnet: 172.31.20.0/24
          gateway: 172.31.20.1
    labels:
      com.example.team: platform
  lan:
    driver: macvlan
    driver_opts: { parent: eth0 }
    ipam: { config: [{ subnet: 192.168.1.0/24, gateway: 192.168.1.1, ip_range: 192.168.1.192/27 }] }
```
- `internal: true` creates an externally isolated network; the networking guide adds that it
  has no default gateway for external connectivity.
- The three bridge `driver_opts` keys above (`com.docker.network.bridge.name`,
  `com.docker.network.driver.mtu`, `com.docker.network.bridge.enable_icc`) are listed in the
  Docker bridge driver documentation; macvlan takes a `parent` option.
- `ipam.config` entries accept `subnet`, `ip_range`, `gateway` and `aux_addresses`.

## Volume driver options
```yaml
volumes:
  nfs:
    driver_opts: { type: nfs, o: "addr=10.0.0.10,rw,nfsvers=4.1", device: ":/exports/app" }
```
The Compose file reference shows the same `type`, `o` and `device` keys for an NFS volume.

## Verify
`docker network ls --filter name=proxy`; `docker network inspect shop_backend`;
`docker volume ls` shows `shop-uploads` and `pgdata` unprefixed.

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main) with Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose file reference and networking guide: `external` semantics and the
error and rejection rules, `name` not being project-scoped, `internal`, `ipam` fields,
volume `driver_opts` NFS example, and `down` never removing external networks or volumes.
Confirmed in the bridge and macvlan driver pages: the three bridge option keys and
macvlan `parent`. Removed as unconfirmed: the exact error and warning message texts, the
claim that internal networks block published-port reachability, and the `docker network
inspect` template.
