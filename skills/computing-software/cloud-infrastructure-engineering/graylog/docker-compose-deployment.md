---
id: computing-software.cloud-infrastructure-engineering.graylog.docker-compose-deployment
name: docker-compose-deployment
category: computing-software
field: cloud-infrastructure-engineering
product: graylog
tags: [docker, compose, container, env-file, vm-max-map-count]
level: practitioner
status: docs-checked
description: "Run Graylog, Data Node and MongoDB with Docker Compose: images, .env secrets, vm.max_map_count and volumes."
sources:
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/docker_installation.htm
  - https://go2docs.graylog.org/current/downloading_and_installing_graylog/graylog_and_docker.htm
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# docker compose deployment

Graylog documents running in Docker through Docker Compose. Images in the Compose file:
- MongoDB: `mongo`
- Data Node: `graylog/graylog-datanode`
- Graylog Enterprise: `graylog/graylog-enterprise`, or Graylog Open: `graylog/graylog`

Steps:
1. Download the example `docker-compose.yml` and `.env.example` from Graylog's GitHub; save the latter as `.env`.
2. Generate `GRAYLOG_PASSWORD_SECRET` (the guide uses `/dev/urandom` piped through `tr` and `head -c` for 96 characters).
3. Generate `GRAYLOG_ROOT_PASSWORD_SHA2` as the sha256 of your chosen password.
4. Put both values in `.env`.
5. Set `vm.max_map_count` to at least 262144 on the Docker host.

Guidance: define Graylog and Data Node environment variables individually, expose only the ports you need, and use external volumes for MongoDB, Data Node and Graylog so data survives restarts.

## Checked

2026-11-04. Confirmed against Run Graylog in Docker (images, example files from GitHub, .env, secret generation, vm.max_map_count of at least 262144) and Graylog and Docker (individually defined variables, exposing only needed ports, external volumes). Removed: the claim that images do not use the latest tag (not on the pages).

Method: documentation only; no commands were run.
