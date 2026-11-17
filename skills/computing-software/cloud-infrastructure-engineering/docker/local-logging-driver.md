---
id: computing-software.cloud-infrastructure-engineering.docker.local-logging-driver
name: local-logging-driver
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, logging-driver, local-log-driver, log-rotation, json-file, daemon-json, docker-logs]
level: practitioner
status: docs-checked
description: "Use the local logging driver for compressed, auto-rotated container logs: defaults, max-size/max-file/compress options, daemon-wide setup, and when json-file is still needed."
sources: ["https://docs.docker.com/engine/logging/drivers/local/", "https://docs.docker.com/engine/logging/configure/", "https://docs.docker.com/engine/logging/drivers/json-file/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# The local logging driver

`json-file` (the default) never rotates unless configured, so hosts fill up. `local` rotates
and compresses **by default** and stores logs in a format optimised for low overhead.

## Defaults
| Option | Default | Meaning |
|---|---|---|
| `max-size` | `20m` | Rotate when a file reaches this size |
| `max-file` | `5` | Files kept (so 100 MB per container by default before compression) |
| `compress` | `true` | Rotated files gzip-compressed |

## Enable host-wide
```json
{
  "log-driver": "local",
  "log-opts": { "max-size": "50m", "max-file": "3" }
}
```
```bash
sudo dockerd --validate --config-file /etc/docker/daemon.json && sudo systemctl restart docker
```
Applies to containers **created** after the change; recreate existing ones
(`docker compose up -d --force-recreate`).

Per container / Compose:
```bash
docker run -d --log-driver local --log-opt max-size=10m --log-opt max-file=10 nginx
```
```yaml
services:
  web:
    logging:
      driver: local
      options: { max-size: "10m", max-file: "10" }
```

## When json-file is still the right choice
- Log shippers or tools that tail the container log files directly and parse JSON lines. The
  `local` driver files are meant to be accessed only by the Docker daemon, and external tools
  can interfere with logging. Use `json-file` with rotation there, or a remote logging driver.

## Verify
```bash
docker inspect -f '{{.HostConfig.LogConfig.Type}} {{json .HostConfig.LogConfig.Config}}' <c>
docker logs --tail 20 <c>          # works the same for local and json-file
```

## Gotchas
- `docker logs` reads only what is still on disk; aggressive rotation loses history.
- The files are for exclusive use by the Docker daemon; do not parse or edit them.
- `local` is a bash reserved keyword, so quote it in scripts.
- Drivers that cannot read logs back (for example splunk or fluentd) still work with `docker logs`
  thanks to dual logging, which uses the `local` driver as a cache with its own `cache-*` options.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine docs (docs.docker.com, docker/docs main).
Confirmed against the local driver, json-file driver, logging configure and dual-logging pages: `max-size` 20m,
`max-file` 5, `compress` on by default, daemon.json and `docker run` syntax, existing containers keeping their old
configuration, the warning that the log files are for daemon-only access, and the dual-logging cache options.
Removed: the protobuf format claim, specific shipper tool names and the on-disk log directory paths, which the
docs do not cover.

Method: documentation only; no commands were run.
