---
id: computing-software.cloud-infrastructure-engineering.docker.compose-default-network-and-resource-naming
name: compose-default-network-and-resource-naming
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose-networks, default-network, network-name, compose-project-name, container-naming, compose-volumes]
level: practitioner
status: verified
description: "How Compose names networks, volumes and containers (<project>_default, <project>-<service>-1), customising the default network, fixed names via name:, and cross-project sharing."
sources: ["https://docs.docker.com/compose/how-tos/networking/", "https://docs.docker.com/reference/compose-file/networks/#name", "https://docs.docker.com/reference/compose-file/volumes/#name", "https://docs.docker.com/compose/how-tos/project-name/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose default network and resource naming

## Defaults
| Resource | Name |
|---|---|
| Project | top-level `name:`, `-p`, `COMPOSE_PROJECT_NAME`, else the directory name (lowercased, sanitised) |
| Default network | `<project>_default` |
| Declared network `backend` | `<project>_backend` |
| Volume `pgdata` | `<project>_pgdata` |
| Containers | `<project>-<service>-<n>` (Compose v2 uses dashes; not run, the daemon is down) |

Every service joins `<project>_default` unless it declares `networks:`; service names are DNS
names on it.

## Customise the default network
```yaml
networks:
  default:
    name: shop-net                     # literal name, no project prefix
    driver: bridge
    driver_opts:
      com.docker.network.driver.mtu: "1400"
    ipam:
      config: [{ subnet: 172.28.0.0/16 }]
```
Or reuse an existing network as the default:
```yaml
networks:
  default:
    name: proxy
    external: true
```

## Fixed names (no prefix)
```yaml
volumes:
  pgdata:
    name: shop-pgdata
services:
  db:
    container_name: shop-db          # prevents scaling; avoid unless required
```

## Why it matters
- Two checkouts of the same repo in directories with the same name share a project and stomp on
  each other's containers; set `name:` in compose.yaml or `-p`.
- Renaming the directory or project creates **new** empty volumes (`newname_pgdata`) and the
  data seems lost; it is still in `oldname_pgdata`.
- Cross-project communication needs a shared external network; project default networks are
  isolated from each other.

## Inspect
```bash
docker compose config | yq '.name, .networks, .volumes'
docker network ls --filter label=com.docker.compose.project=shop
docker inspect -f '{{json .NetworkSettings.Networks}}' shop-web-1 | jq 'keys'
```

## Gotchas
- Project names must be lowercase letters, digits, dashes and underscores, starting with a
  letter or digit.
- `container_name` must be unique host-wide; a second project with the same value fails. Compose also refuses `container_name` together with `deploy.replicas` > 1: `can't set container_name and worker as container name must be unique: invalid compose project` (checked via `config` and `up --dry-run`). Names must be at least two characters (`'w' does not match pattern '[a-zA-Z0-9][a-zA-Z0-9_.-]+'`).

## Checked
Run on Windows 11 with Docker Compose v2.39.1 (`docker compose config` and `--dry-run`, no daemon needed): default network `<project>_default`, declared network `<project>_backend`, volume `<project>_<name>`, fixed `name:` for network and volume, a customised default network with `driver_opts` and `ipam`, `external: true` on the default network (name `proxy`, not prefixed), project-name derivation from a directory with capitals, space and underscore (`shopdir_x`), and the container_name validation above. Not run: actual container names, `docker network ls`, `docker inspect`, cross-project communication, volume loss after renaming a directory, Linux.
