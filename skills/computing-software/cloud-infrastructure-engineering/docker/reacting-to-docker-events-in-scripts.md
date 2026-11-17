---
id: computing-software.cloud-infrastructure-engineering.docker.reacting-to-docker-events-in-scripts
name: reacting-to-docker-events-in-scripts
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, docker-events, events-automation, health-status-event, oom, alerting, events-filter]
level: advanced
status: docs-checked
description: "Build event-driven automation on docker events: stream die/oom/health_status as JSON, alert or restart with a supervised loop, handle reconnects, and avoid missed events."
sources: ["https://docs.docker.com/reference/cli/docker/system/events/", "https://docs.docker.com/reference/api/engine/version/v1.56/#tag/System/operation/SystemEvents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reacting to docker events in scripts

`docker events` streams daemon events in real time. It is the cheapest way to alert on
crashes, OOM kills and unhealthy containers on standalone hosts.

## Stream the interesting events
```bash
docker events --format '{{json .}}' \
  --filter type=container \
  --filter event=die --filter event=oom --filter event=health_status \
  --filter event=restart
```
With `--format '{{json .}}'` events stream as JSON Lines. The default text output of a `die`
event includes `exitCode`, `image` and `name` attributes. The container events include `die`,
`oom`, `health_status`, `kill`, `restart`, `start` and `stop`. Filters: using the same filter
key several times is a logical OR, different keys are ANDed.

## Alerting loop
```bash
#!/usr/bin/env bash
set -u
since=$(date +%s)                     # --since takes Unix timestamps, dates or durations such as 10m
while true; do
  docker events --since "$since" \
    --format '{{.Type}} {{.Action}} {{.Actor.Attributes.name}} {{.Actor.Attributes.exitCode}}' \
    --filter type=container --filter event=die --filter event=oom --filter event=health_status |
  while read -r line; do
    since=$(date +%s)
    curl -fsS -X POST -H 'Content-Type: application/json' \
      -d "{\"text\":\"$(hostname): $line\"}" "$WEBHOOK_URL" || true
  done
  sleep 2                             # the stream ends if the daemon restarts; reconnect
done
```
Run it as a service that restarts on failure. The `since` update happens inside the pipe's
subshell, so it does not survive the loop; persist it to a file if exact resume matters.

## Auto-remediation (carefully)
Restarting a container when it reports unhealthy is possible from the same loop; add a rate
limit or you build a restart storm.

## Gotchas
- Docker's reference says only the last 256 log events are returned for a `--since` query, so
  it cannot replay far back; use filters to limit what is returned.
- `die` events also occur for normal stops (the exit code is in the event attributes), so filter
  or inspect the exit code to reduce noise.
- For fleets, prefer metrics/log pipelines (cAdvisor, Loki, OTel) over per-host scripts.

## Checked

2026-10-26 against Docker docs (docker/docs main, 2026-10-23), docker/cli system events reference, Compose and Scout CLI reference data, dive, uv and distroless READMEs, action repositories at their latest releases. Confirmed in the docker events reference (docker/cli system_events.md): filters and OR/AND semantics, container event names (die, oom, health_status, restart and others), --since/--until formats, --format with {{json .}} giving JSON Lines, die example with exitCode/image/name, 256-event limit for history. Removed the jq-based parsing, the 1000-entry buffer figure (the reference says 256), health_status action strings, Compose label names, OOM behaviour and the autoheal reference.

Method: documentation only; no commands were run.
