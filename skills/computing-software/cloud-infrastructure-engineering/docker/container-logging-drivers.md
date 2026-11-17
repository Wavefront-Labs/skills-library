---
id: computing-software.cloud-infrastructure-engineering.docker.container-logging-drivers
name: container-logging-drivers
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, logging-driver, json-file, journald, syslog, fluentd, gelf, awslogs, splunk-driver, log-opts, max-size, max-file, dual-logging, docker-logs-compat, log-rotation, stdout-stderr]
level: practitioner
status: docs-checked
description: "Docker logging driver choice and config: json-file rotation that must be set explicitly, why docker logs stops working with external drivers, and the dual-logging workaround."
sources: ["https://docs.docker.com/engine/logging/configure/", "https://docs.docker.com/engine/logging/drivers/json-file/", "https://docs.docker.com/engine/logging/dual-logging/", "https://docs.docker.com/engine/logging/drivers/fluentd/", "https://docs.docker.com/engine/logging/drivers/syslog/", "https://docs.docker.com/engine/logging/drivers/gelf/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Container logging drivers

**Goal:** logs rotate instead of filling the disk, `docker logs` keeps working for local
debugging even after wiring up shipping to a real aggregator, and the driver choice matches
how the container actually produces output.

## `json-file` — the default, and its one critical setting
Unconfigured `json-file` performs no rotation (`max-size` defaults to -1, unlimited, and
`max-file` to 1), so every log line stays on disk, one JSON object per line. A single chatty
container with no limit can fill the host's disk, and the Docker docs recommend the `local`
driver (which rotates by default) to prevent disk exhaustion:
```json
{ "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" } }
```
in `/etc/docker/daemon.json` (daemon-wide default, see
`docker-daemon-configuration-and-hardening`) or per-container/per-Compose-service if
different services need different retention. `max-size` is per-file; `max-file` is how
many rotated files are kept and is only effective when `max-size` is also set. Option values
in `daemon.json` must be quoted strings. Changing the daemon default affects only newly
created containers.

## Other drivers, and what you lose
Switching to `syslog`, `journald`, `gelf`, `fluentd`, `awslogs`, `splunk`, etc. ships logs
to that destination. The `none` driver makes `docker logs` return nothing. For drivers that
cannot read logs back, Docker Engine enables **dual logging** automatically: the `local`
driver acts as a cache so `docker logs` still works.
- **Dual logging cache**: rotated by default at 5 files of 20 MB each per container. Tune it
  with `cache-max-size`, `cache-max-file`, `cache-compress`, or turn it off with
  `cache-disabled=true`; with the cache disabled, `docker logs` on a remote-only driver fails
  with `configured logging driver does not support reading`.
- `local`, `json-file` and `journald` support reading logs natively.
- `mode=non-blocking` with `max-buffer-size` (default `1m`) on any driver stops a slow or
  unreachable log destination from blocking the container's stdout writes. When the buffer
  is full new messages are dropped. The default `mode=blocking` delivers directly and can
  stall the application if the sink degrades.

## What actually gets captured
Docker logging drivers only capture what the container writes to **stdout/stderr of PID 1**
(or whatever process `docker run`'s entrypoint execs into). An app that logs to a file
inside the container, or forks a child process that does its own stdout redirection, won't
appear in `docker logs` regardless of driver — fix at the application config (log to
stdout) rather than fighting the logging driver, which is the standard container logging
convention for exactly this reason.

## Syslog/GELF/Fluentd specifics worth knowing
- `syslog` driver options (`syslog-address`, `syslog-facility`, `tag`) route to a remote
  syslog server; `syslog-address` accepts `tcp`, `udp`, `tcp+tls`, `unix` and `unixgram`
  schemes, with `syslog-tls-ca-cert`, `syslog-tls-cert`, `syslog-tls-key` and
  `syslog-tls-skip-verify` applying only to `tcp+tls`.
- The `gelf` driver does not support TLS for TCP connections; messages sent to TLS-protected
  inputs can silently fail.
- With the `fluentd` driver, if the container cannot connect to the Fluentd daemon it stops
  immediately unless `fluentd-async` is set (default `false`).

## Verify
After setting `max-size`/`max-file`, generate enough log volume to force a rotation and
confirm the container's log files are capped and rotated, not one ever-growing log. For a
non-`json-file` driver, confirm logs actually arrive at the
destination (not just that the driver was accepted) and separately confirm whether `docker
logs` still works or was knowingly traded away.

## Checked

Date: 2026-10-24. Documentation release: Docker Engine docs (docs.docker.com, docker/docs main).
Confirmed against the logging configure, json-file, dual-logging, fluentd, syslog and gelf pages:
json-file defaults (`max-size` -1, `max-file` 1, `max-file` effective only with `max-size`), dual logging
being automatic with its `cache-*` options and defaults, `max-buffer-size` default 1m, syslog address schemes
and TLS options, gelf TCP TLS limitation, fluentd-async default and startup behaviour. Removed: the claim that only
json-file and journald support `docker logs`, the Docker 20.10 version gate, and the host log path, none of which
the docs state.

Method: documentation only; no commands were run.
