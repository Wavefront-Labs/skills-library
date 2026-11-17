---
id: computing-software.cloud-infrastructure-engineering.fluentd.docker-logging-driver
name: docker-logging-driver
category: computing-software
field: cloud-infrastructure-engineering
product: fluentd
tags: [cloud-infrastructure-engineering, fluentd, docker, logging-driver, fluentd-address, log-opt, concat, parser]
level: practitioner
status: docs-checked
description: "Send container stdout to Fluentd with Docker's fluentd logging driver: fluentd-address and tag options, record fields, parsing JSON and joining multiline logs."
sources:
  - https://docs.fluentd.org/container-deployment/docker-logging-driver
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker fluentd logging driver
Configure Fluentd to listen with a `forward` source (`port 24224`, `bind 0.0.0.0`), then run containers with `--log-driver=fluentd`. The container will not start if it cannot connect to Fluentd, which by default is expected on TCP 24224 locally. The driver does not support sub-second precision.

Each event is tagged with the 64-character `container_id` by default and carries `container_id`, `container_name`, `source` and `log`.

Driver options via `--log-opt`:
- `fluentd-address=<ip>:<port>`, for example `192.168.2.4:24225`.
- `tag=docker.my_new_tag`; may use `{{.ID}}`, `{{.FullID}}`, `{{.Name}}`.

Parse application JSON from the `log` field:
```
<filter docker.**>
  @type parser
  key_name log
  reserve_data true
  <parse>
    @type json
  </parse>
</filter>
```
Join multiline output with the third-party `fluent-plugin-concat` (install in a custom image via `fluent-gem install fluent-plugin-concat`):
```
<filter docker.**>
  @type concat
  key log
  stream_identity_key container_id
  multiline_start_regexp /^-e:2:in `\/'/
  multiline_end_regexp /^-e:4:in/
</filter>
```
For production the page says to use an orchestrator, with Kubernetes having the best Fluentd integration.

## Checked

2026-11-04: read the fetched text of https://docs.fluentd.org/container-deployment/docker-logging-driver and confirmed: driver options, default tag, record fields, filter examples, sub-second precision note. Removed or reworded: nothing.

Method: documentation only; no commands were run.
