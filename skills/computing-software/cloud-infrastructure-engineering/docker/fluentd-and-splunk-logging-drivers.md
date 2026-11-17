---
id: computing-software.cloud-infrastructure-engineering.docker.fluentd-and-splunk-logging-drivers
name: fluentd-and-splunk-logging-drivers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, logging-driver, fluentd, fluentd-driver-options, splunk-logging, splunk-hec, log-shipping]
level: advanced
status: docs-checked
description: "Ship container logs with the fluentd and splunk drivers: addresses, async and buffer options, tags, HEC tokens and TLS, and avoiding containers that block or fail to start."
sources: ["https://docs.docker.com/engine/logging/drivers/fluentd/", "https://docs.docker.com/engine/logging/drivers/splunk/", "https://docs.docker.com/engine/logging/dual-logging/", "https://docs.docker.com/engine/logging/log_tags/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# fluentd and splunk logging drivers

## fluentd driver (writes to a Fluentd forward input)
```bash
docker run -d --log-driver fluentd \
  --log-opt fluentd-address=tcp://127.0.0.1:24224 \
  --log-opt fluentd-async=true \
  --log-opt fluentd-buffer-limit=524288 \
  --log-opt fluentd-retry-wait=1s --log-opt fluentd-max-retries=30 \
  --log-opt tag='docker.{{.Name}}' \
  --log-opt labels=app,env --log-opt env=GIT_SHA \
  myapp
```
Key options:
| Option | Notes |
|---|---|
| `fluentd-address` | `host:port`, `tcp://`, or `unix:///path.sock` (default `localhost:24224`) |
| `fluentd-async` | `true`: connect in the background and buffer until connected (default `false`: the container stops if it cannot connect) |
| `fluentd-buffer-limit` | Number of events buffered in memory (default 1048576); when full, the log call fails |
| `fluentd-retry-wait` / `fluentd-max-retries` | Wait between retries (default 1 second) / maximum retries (default 4294967295) |
| `fluentd-sub-second-precision` | Nanosecond timestamps (default `false`) |
| `tag` | Go template: `{{.Name}}`, `{{.ID}}`, `{{.FullID}}`, `{{.ImageName}}`, `{{.DaemonName}}` |
| `labels`, `env`, `labels-regex`, `env-regex` | Add container labels/env to each record |

Collector side: run a Fluentd daemon with a forward input listening on the address you set
(the driver connects to `localhost:24224` by default). Records arrive with `container_id`,
`container_name`, `source` (`stdout` or `stderr`) and `log`.

## splunk driver (HTTP Event Collector)
```json
{
  "log-driver": "splunk",
  "log-opts": {
    "splunk-url": "https://splunk.example.com:8088",
    "splunk-token": "<hec-token>",
    "splunk-index": "containers",
    "splunk-sourcetype": "docker:json",
    "splunk-format": "json",
    "splunk-verify-connection": "false",
    "splunk-gzip": "true",
    "splunk-capath": "/path/to/splunk-ca.pem",
    "tag": "{{.Name}}/{{.ID}}"
  }
}
```
`splunk-token` and `splunk-url` are required. `splunk-verify-connection` defaults to `true`
(verify at start that Docker can reach Splunk); `false` skips that check. `splunk-gzip`
defaults to `false`. `splunk-format`: `inline` (default), `json`, `raw`. `splunk-capath` is the
path to the root certificate.

## Avoid outages caused by logging
- Without `fluentd-async`, the container stops if it cannot connect to Fluentd. For splunk,
  `splunk-verify-connection` defaults to `true`, so an unreachable Splunk is detected at start.
  `mode=non-blocking` with `max-buffer-size` (default `1m`) keeps a slow sink from blocking the
  application.
- Dual logging (automatic for drivers that cannot read logs back) keeps `docker logs` working
  with these drivers.
- Keep the HEC token in the daemon configuration rather than in Compose files committed to Git.

## Verify
```bash
docker inspect -f '{{.HostConfig.LogConfig}}' <c>
docker logs <c> | tail -3                       # via the dual logging cache
```
Then search the collector for `container_name` of a test container.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine docs (docs.docker.com, docker/docs main).
Confirmed against the fluentd, splunk, dual-logging and log tags pages: fluentd option names and defaults
(address default localhost:24224, tcp default with unix socket support, async default false, retry-wait, max-retries,
sub-second precision), splunk required options, `splunk-format` default inline, `splunk-verify-connection` default
true, `splunk-gzip` default false, the tag template fields, and the recorded fields. Corrected: `fluentd-buffer-limit`
is an event count not bytes, and `splunk-verify-connection` defaults to true. Removed: the Fluent Bit forward input
configuration and source link (not checked), the `failed to initialize logging driver` message, the Engine 20.10 gate
and a host-specific certificate path.

Method: documentation only; no commands were run.
