---
id: computing-software.cloud-infrastructure-engineering.docker.compose-networks-and-volumes
name: compose-networks-and-volumes
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, compose-networks, compose-volumes, top-level-networks, top-level-volumes, external, long-syntax, bind, tmpfs, aliases, internal, compose-down-v]
level: practitioner
status: docs-checked
description: "Declaring networks and volumes in a Compose file: default network, per-service networks, external resources, short and long volume syntax, naming and labels, and what down -v deletes."
sources: ["https://docs.docker.com/reference/compose-file/networks/", "https://docs.docker.com/reference/compose-file/volumes/", "https://docs.docker.com/reference/compose-file/services/#volumes", "https://docs.docker.com/compose/how-tos/networking/", "https://docs.docker.com/reference/cli/docker/compose/down/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Compose networks and volumes

**Goal:** a Compose file whose services are segmented the way you intend, whose data
survives `down`, and which does not silently create or orphan resources.

## Networks
Compose creates `<project>_default` and attaches every service to it unless the service
lists `networks:`. Service names resolve on it. To segment:
```yaml
services:
  web:
    networks:
      frontend:
      backend:
        aliases: [api-internal]        # extra DNS name on this network only
        gw_priority: 100               # this network supplies the default gateway
  db:
    networks: [backend]
networks:
  frontend:
  backend:
    internal: true                     # externally isolated network
    driver: bridge
    driver_opts:
      com.docker.network.bridge.name: br-backend
    ipam:
      config:
        - subnet: 10.42.0.0/24
```
- If `networks` is empty or absent, the service is implicitly connected to `default`. A
  service that lists networks is connected to those networks (list `default` too if you
  want it).
- `priority` sets the order in which Compose connects the container to its networks; the
  reference states it does not choose the default gateway (use `gw_priority`) and cannot
  determine the interface name (`eth0`).
- `name:` sets a custom network name that is not scoped with the project name. `external:
  true` means Compose neither creates nor removes it and returns an error if it does not
  exist; every other attribute except `name` is invalid for an external network.
- `network_mode` (`bridge`, `none`, `host`, `service:{name}`, `container:{name}`) and
  `networks` cannot be combined: Compose rejects a file with both. `service:{name}` shares
  that service's network access.
- A static `ipv4_address` needs an `ipam` entry with a subnet covering the address.
- `ports:` publishes to the host. `expose:` declares ports reachable by linked services
  that should not be published to the host.

## Volumes
```yaml
services:
  db:
    volumes:
      - pgdata:/var/lib/postgresql/data            # named volume
      - ./init:/docker-entrypoint-initdb.d:ro      # bind mount (relative to the compose file)
      - type: tmpfs
        target: /tmp
        tmpfs: {size: 104857600}
      - type: bind
        source: ./config
        target: /etc/app
        read_only: true
        bind: {create_host_path: false}            # fail instead of creating the directory
      - type: volume
        source: cache
        target: /cache
        volume: {nocopy: true}                     # don't copy data from the container on creation
volumes:
  pgdata:
  cache:
    external: true
    name: build-cache
  nfsdata:
    driver: local
    driver_opts:
      type: nfs
      o: addr=10.0.0.5,rw,nfsvers=4
      device: ":/export/data"
```
- Short syntax is `VOLUME:CONTAINER_PATH[:ACCESS_MODE]`; `VOLUME` is a host path (bind
  mount) or a volume name. Start relative host paths with `.` or `..` to avoid ambiguity with
  named volumes.
- For bind mounts, the short syntax creates a directory at the source path on the host if it
  does not exist (backward compatibility). Long syntax with `create_host_path: false`
  prevents that.
- `nocopy` disables copying of data from a container when a volume is created; `subpath`
  mounts a path inside a volume.
- Project volumes are created as `<project_name>_<key>` and labelled
  `com.docker.compose.project` and `com.docker.compose.volume`. A `name:` is used as is.
- The `tmpfs` option `size` is in bytes (numeric, or with a byte unit).

## What `down` removes
| Command | Containers | Networks | Named volumes | Anonymous volumes |
|---|---|---|---|---|
| `compose down` | yes | those in the file and the default network (never external) | no | no |
| `compose down -v` | yes | same | declared in the file (never external) | yes, those attached to containers |
| `compose rm -v` | stopped ones | no | no | yes, those attached to the removed containers |

- `compose down --rmi local` also removes images that have no custom tag (`all` removes all
  images used by services).
- `compose up --renew-anon-volumes` (`-V`) recreates anonymous volumes instead of retrieving
  data from the previous containers.
- `compose down --remove-orphans` removes containers for services no longer defined in the
  file.

## Verify
```bash
docker compose config                         # fully resolved: every volume/network name visible
docker volume ls --filter label=com.docker.compose.project=<project>
docker compose down && docker volume ls       # named volumes are still listed
```

## Checked
Date 2026-10-23. Documentation release: Docker docs (docker/docs main) with Compose v5.6.1.
Method: documentation only; no commands were run.
Confirmed in the Compose file reference: implicit `default` network, `priority` and
`gw_priority` semantics (this corrects an earlier claim that `priority` selects the default
route and `eth0`), `network_mode` versus `networks`, `ipv4_address` with `ipam`, `external`
and `name` rules, short and long volume syntax, `create_host_path`, `nocopy`, `subpath`,
tmpfs `size`, volume labels and naming. Confirmed in the Compose CLI reference: `down`,
`rm -v` and `up -V` options and descriptions. Removed as unconfirmed: the ownership of
auto-created host directories, `volumes_from` and Windows path-conversion remarks, the exact
error texts and the claim that `expose` is documentation only (the reference describes it
as declaring ports for linked services).
