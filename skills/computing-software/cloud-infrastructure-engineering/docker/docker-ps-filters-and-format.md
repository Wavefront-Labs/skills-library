---
id: computing-software.cloud-infrastructure-engineering.docker.docker-ps-filters-and-format
name: docker-ps-filters-and-format
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-ps, ps-filter, ps-format, container-lifecycle, go-template, scripting]
level: practitioner
status: docs-checked
description: "Find containers fast with docker ps filters (status, exited, health, label, ancestor, network, volume, publish) and --format templates or JSON for scripts and dashboards."
sources: ["https://docs.docker.com/reference/cli/docker/container/ls/", "https://github.com/docker/cli/blob/master/docs/reference/commandline/docker.md", "https://docs.docker.com/engine/cli/filter/", "https://docs.docker.com/engine/cli/formatting/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker ps filters and format

## Filters
```bash
docker ps -a --filter status=exited --filter exited=137      # exit code 137
docker ps --filter health=unhealthy
docker ps --filter label=com.docker.compose.project=shop
docker ps --filter ancestor=nginx:1.27                       # created from this image (or descendants)
docker ps --filter network=backend
docker ps --filter volume=pgdata                             # running containers mounting this volume
docker ps --filter publish=8080                              # who publishes host port 8080
docker ps --filter expose=5432/tcp
docker ps --filter name=web                                  # substring match on the name
docker ps -a --filter before=web-1 --filter since=db-1
docker ps --filter is-task=true                              # Swarm task containers
```
Status values: `created`, `restarting`, `running`, `removing`, `paused`, `exited`, `dead`.

## Format
```bash
docker ps --format 'table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}'
docker ps --format '{{.Names}} {{.Label "com.docker.compose.service"}}'
docker ps --format json                                        # one JSON object per container
docker ps -q --filter status=exited                          # IDs only
docker ps -s --format '{{.Names}} {{.Size}}'                  # container size on disk
docker ps --no-trunc --format '{{.Command}}'
```
Placeholders: `.ID .Image .Command .CreatedAt .RunningFor .Ports .State .Status .Size .Names
.Labels .Label "key" .Mounts .Networks .HealthStatus`.

Default format for your shell: `~/.docker/config.json`
```json
{ "psFormat": "table {{.Names}}\t{{.Status}}\t{{.Image}}\t{{.Ports}}" }
```

## Recipes
```bash
# containers restarting in a loop
docker ps --filter status=restarting --format '{{.Names}} {{.Status}}'
```

## Gotchas
- Without `-a`, stopped containers are hidden, so `status=exited` returns nothing.

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: filters id, name, label, exited (with `--all`), status (values created, restarting, running, removing, paused, exited, dead), ancestor, before, since, volume and network (running containers), publish/expose, health (starting, healthy, unhealthy, none), is-task; `name` matches a substring; `--format` values table, json and the placeholders `.ID .Image .Command .CreatedAt .RunningFor .Ports .State .Status .HealthStatus .Size .Names .Labels .Label .Mounts .Networks`; `psFormat` in the CLI config file; `-a` shows stopped containers. Removed: regex anchor in the name filter, AND/OR rule (not documented for `ps`), ancestor retag claim, size-walk claim, jq and xargs pipelines, outdated-image shell loop.
Method: documentation only; no commands were run.
