---
id: computing-software.cloud-infrastructure-engineering.docker.non-blocking-logging-and-log-tags
name: non-blocking-logging-and-log-tags
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, logging-driver, log-driver, non-blocking-logging, max-buffer-size, log-tag-template, log-labels, syslog, fluentd]
level: advanced
description: "Stop slow log backends from blocking containers with mode=non-blocking and max-buffer-size, and enrich log records via tag templates and labels/env options."
sources: ["https://docs.docker.com/engine/logging/configure/#configure-the-delivery-mode-of-log-messages-from-container-to-log-driver", "https://docs.docker.com/engine/logging/log_tags/", "https://docs.docker.com/engine/logging/drivers/json-file/#options", "https://docs.docker.com/engine/logging/drivers/gelf/", "https://docs.docker.com/engine/logging/drivers/journald/"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Non-blocking logging and log tags

## Blocking vs non-blocking
Default `mode=blocking`: the container's stdout write blocks until the driver accepts the
message. If fluentd/syslog/awslogs is slow or down, **the application stalls** on
`write()` - request latency spikes, health checks fail.

```sh
docker run --log-driver fluentd \
  --log-opt fluentd-address=127.0.0.1:24224 \
  --log-opt mode=non-blocking --log-opt max-buffer-size=8m app:1
```
```json
{ "log-driver": "fluentd",
  "log-opts": { "mode": "non-blocking", "max-buffer-size": "8m", "fluentd-async": "true" } }
```
- Messages go to an intermediate per-container buffer (`max-buffer-size`, default `1m`);
  when it is full, **new messages are not enqueued** (dropped). Trade: availability over
  completeness.
- fluentd also has `fluentd-async` (default `false`; connect in the background and buffer
  until connected, otherwise the container stops if it cannot reach Fluentd) and
  `fluentd-buffer-limit` (a count of events, default 1048576).

## Tag templates
```sh
--log-opt tag="{{.ImageName}}/{{.Name}}/{{.ID}}"
```
Available: `{{.ID}}` (12 chars), `{{.FullID}}`, `{{.Name}}`, `{{.ImageID}}`, `{{.ImageFullID}}`,
`{{.ImageName}}`, `{{.DaemonName}}`. Default tag is `{{.ID}}`. syslog and gelf append the
tag to the `APP-NAME`, fluentd uses it as the message tag, journald sets `CONTAINER_TAG` and
`SYSLOG_IDENTIFIER` from it.
Compose: `logging: { options: { tag: "{{.Name}}" } }`.

## labels / env / *-regex options
```sh
docker run --label team=payments -e DEPLOY_ENV=prod \
  --log-opt labels=team --log-opt env=DEPLOY_ENV --log-opt env-regex='^(SERVICE|VERSION)$' app:1
```
Selected container labels/env vars are attached to log records (for example gelf adds them
to the `extra` fields), so the aggregator can filter without parsing names. `labels-regex`
matches labels by pattern, `env-regex` matches environment variables.

## Gotchas
- Non-blocking drops are invisible to the application, so size `max-buffer-size` with care.
- Changing log options needs container re-creation; daemon.json changes only affect new containers.
- Don't put secrets in env vars that you then attach to logs with `env=`.

## Verify
```sh
docker inspect -f '{{json .HostConfig.LogConfig}}' app
docker logs app      # works for drivers without read support via the dual logging cache
```
Kill the log receiver and confirm the app's latency is unaffected.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine docs (docs.docker.com, docker/docs main).
Confirmed against the logging configure, log tags, fluentd, journald, gelf and syslog pages: blocking default and
non-blocking buffer behaviour, `max-buffer-size` default 1m, the tag template fields and default `{{.ID}}`,
where each driver puts the tag, `fluentd-async` default and startup behaviour, `fluentd-buffer-limit` being an
event count. Corrected: the gelf tag is appended to `APP-NAME` (not a `_tag` field) and `fluentd-buffer-limit`
counts events, not bytes. Removed: the sizing example, the Engine 20.10 gate, the json-file `attrs` claim and the
dockerd log-message string, which no documentation page states.

Method: documentation only; no commands were run.
