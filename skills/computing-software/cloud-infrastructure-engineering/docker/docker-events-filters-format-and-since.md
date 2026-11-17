---
id: computing-software.cloud-infrastructure-engineering.docker.docker-events-filters-format-and-since
name: docker-events-filters-format-and-since
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-events, events-filter, events-since, events-format, container-events, oom, health-status, restart-loop, monitoring]
level: practitioner
status: docs-checked
description: "Use docker events precisely: filter keys and AND/OR rules, --since/--until replay windows, Go-template and JSON output, and catching dies, OOMs, health changes and exec."
sources: ["https://docs.docker.com/reference/cli/docker/system/events/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# docker events: filters, format and time windows

## Filters
```bash
docker events --filter type=container --filter event=die --filter event=oom
```
- Same key repeated = **OR** (`event=die` or `event=oom`); different keys = **AND**.
- Keys: `type` (container, image, volume, network, daemon, plugin, service, node, secret,
  config), `event`, `container` (name or id), `image`, `label` (`label=com.docker.compose.project=shop`),
  `network`, `volume`, `plugin`, `daemon`, `node`, `service`, `secret`, `config`, `scope` (local|swarm).
- Compose project scope: `--filter label=com.docker.compose.project=<name>`.

## Time windows
```bash
docker events --since 30m --until 0s       # replay, then exit
docker events --since '2026-10-16T09:00:00' --until '2026-10-16T09:15:00'
docker events --since 1697443200            # Unix seconds
```
- `--since` and `--until` take Unix timestamps, date-formatted timestamps or Go durations relative to the client machine's time.
- Without `--until` the command replays from `--since` then keeps streaming.
- Only the last 256 events are returned, so `--since 24h` on a busy host can return far less than 24 hours. Use filters to narrow the result, and ship the
  stream somewhere continuously if you need history.

## Output format
```bash
docker events --format '{{.Time}} {{.Type}} {{.Action}} {{.Actor.Attributes.name}} exit={{.Actor.Attributes.exitCode}}'
docker events --format '{{json .}}'      # JSON Lines, one event per line
```
Run once with `{{json .}}` to see the available fields. In the docs' sample output the attributes include `name`, `image`, `exitCode` on die and `signal` on kill.

## Recipes
Crash/restart loop watch:
```bash
docker events -f type=container -f event=die -f event=restart \
  --format '{{.Time}} {{.Actor.Attributes.name}} {{.Action}} {{.Actor.Attributes.exitCode}}'
```
Exit 137 is SIGKILL (128+9); an `oom` event before the `die` points to a memory-limit kill.

Health flaps:
```bash
docker events -f event=health_status --format '{{.Actor.Attributes.name}} {{.Action}}'
```
Audit interactive access: `-f event=exec_create --format '{{.Time}} {{.Actor.Attributes.name}} {{.Actor.Attributes.execID}}'`.

Image and volume churn (who deleted what): `-f type=image -f event=delete -f event=untag`,
`-f type=volume -f event=destroy`.

## Running it as a service
```ini
# /etc/systemd/system/docker-events-log.service
[Service]
ExecStart=/usr/bin/docker events --format '{{json .}}'
Restart=always
```
The unit's output goes to the journal, which then holds the history.

## Verify
```bash
docker events --since 1m --until 0s -f type=container &
docker run --rm alpine false; wait      # shows the container's create, start, die and destroy events
```

## Checked
2026-10-25, against docker/docs engine and swarm pages (repository head 2026-10-23) and docker/cli docs/reference/commandline (master). Confirmed: filter keys config, container, daemon, event, image, label, network, node, plugin, scope, secret, service, type, volume; the same key repeated is OR and different keys are AND; container event names including `die`, `oom`, `health_status`, `exec_create`, `exec_start`, `kill`, `restart`, `destroy`; `--since`/`--until` formats; only the last 256 events are returned; `--format '{{json .}}'` gives JSON Lines; sample output shows `exitCode` and `signal` attributes. Removed: prefix-matching claim for three event names, in-memory and restart-persistence claims, jq pipeline, field list beyond the documented examples, Compose events alias.
Method: documentation only; no commands were run.
