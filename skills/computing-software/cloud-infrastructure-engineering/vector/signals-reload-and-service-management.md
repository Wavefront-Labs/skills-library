---
id: computing-software.cloud-infrastructure-engineering.vector.signals-reload-and-service-management
name: signals-reload-and-service-management
category: computing-software
field: cloud-infrastructure-engineering
product: vector
tags: [management, sighup, sigterm, systemctl, docker, kubernetes, exit-codes, vector]
level: practitioner
status: docs-checked
description: "Start, stop and reload Vector under systemd, Docker and Kubernetes and know its signals and exit codes."
sources:
  - https://vector.dev/docs/administration/management/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Signals: `SIGHUP` reloads configuration on the fly; `SIGTERM` starts graceful shutdown. Exit codes: 0 success, 1 generic error, 78 invalid configuration.

By environment, from the docs:

```bash
# no process manager
killall -s SIGHUP vector
# systemd (apt, dpkg, rpm, yum, pacman installs)
systemctl kill -s HUP --kill-who=main vector.service
sudo systemctl restart vector
# Docker
docker kill --signal=HUP timberio/vector
# Kubernetes (Helm installs)
kubectl rollout restart --namespace vector daemonset/vector-agent
kubectl rollout restart --namespace vector statefulset/vector-aggregator
```

Homebrew uses `brew services start|stop|restart vector`. The Docker examples use image variants alpine, debian (slim) or distroless.

Automatic reload: start with `--watch-config`; `--watch-config-method poll` suits NFS or EFS mounted files.

Practice: validate first (see validate-configuration), then send SIGHUP or let the watcher reload.

Verify that `vector validate` exits with 78 on a bad config.

## Checked

2026-11-03. Read administration/management and reference/cli. Confirmed: SIGHUP reloads, SIGTERM starts graceful shutdown, exit codes 0, 1 and 78, every command in the code block, Homebrew services, the alpine, debian-slim and distroless variants, and `--watch-config-method poll` for NFS/EFS. Removed: the ConfigMap advice and the claim that a bad reload leaves the old topology running (not stated). Note: the management page says the poll interval defaults to 30 while the CLI reference says 60; the CLI skill uses the CLI reference value.

Method: documentation only; no commands were run.
