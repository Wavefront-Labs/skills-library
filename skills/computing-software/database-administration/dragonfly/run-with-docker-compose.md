---
id: computing-software.database-administration.dragonfly.run-with-docker-compose
name: run-with-docker-compose
category: computing-software
field: database-administration
product: dragonfly
tags: [docker-compose, dragonfly, network-mode, nat-overhead]
level: intro
status: docs-checked
description: "Run Dragonfly with the official Docker Compose file and avoid the NAT cost of overlay networks when tuning for performance."
sources:
  - https://raw.githubusercontent.com/dragonflydb/documentation/main/docs/getting-started/docker-compose.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Needs Docker and Docker Compose installed.

```bash
wget https://raw.githubusercontent.com/dragonflydb/dragonfly/main/contrib/docker/docker-compose.yml
docker compose up -d
docker ps | grep dragonfly
docker logs -f docker_dragonfly_1
```

Dragonfly answers both `http` and `redis` requests. Connect with `redis-cli` to `localhost:6379` or visit `http://localhost:6379`.

## Performance tuning

Containerisation adds `NAT` cost. In `docker compose` there is a significant difference between an `overlay` network (docker NAT traversal on every request) and the `host` network. The official `docker-compose.yml` shows the host network setup, and the Compose `network_mode` docs explain the option.

When tuning Dragonfly for performance, consider these NAT costs of containerisation.

## Checked

2026-11-04. Confirmed against the Dragonfly Docker Compose install page: prerequisites, the four commands, http and redis answers, the NAT, overlay and host network note and network_mode pointer. Softened the benchmarking advice to the page's wording (consider the NAT cost).

Method: documentation only; no commands were run.
