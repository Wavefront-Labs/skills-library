---
id: computing-software.cloud-infrastructure-engineering.docker.validating-and-reloading-daemon-json
name: validating-and-reloading-daemon-json
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, daemon-json, dockerd-validate, daemon-reload-sighup, dockerd, live-reload, daemon-config]
level: practitioner
status: docs-checked
description: "Change daemon.json safely: dockerd --validate before restarting, which keys reload live with SIGHUP vs need a restart, and recovering when dockerd refuses to start."
sources: ["https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://docs.docker.com/reference/cli/dockerd/#configuration-reload-behavior", "https://docs.docker.com/engine/daemon/troubleshoot/", "https://docs.docker.com/engine/daemon/", "https://docs.docker.com/desktop/settings-and-maintenance/settings/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Validating and reloading daemon.json

A typo in `/etc/docker/daemon.json` stops dockerd from starting, which on a single host
means every container is down.

## Validate first
```bash
sudo dockerd --validate --config-file=/etc/docker/daemon.json
```
`--validate` validates the daemon configuration and exits. Docker does not start if
`daemon.json` contains invalid JSON.

## Reload without restart (SIGHUP)
```bash
sudo kill -SIGHUP $(pidof dockerd)
```
On Linux the daemon reloads on `SIGHUP` (Windows uses a global event). The daemon still checks for
conflicts with CLI flags; if there are conflicts it fails to reconfigure itself but keeps running.
Options the dockerd reference lists as reloadable: `debug`, `labels`, `live-restore`,
`max-concurrent-downloads`, `max-concurrent-uploads`, `max-download-attempts`,
`default-runtime`, `default-stop-timeout`, `runtimes`, `authorization-plugin`,
`insecure-registries`, `registry-mirrors`, `shutdown-timeout`, `features`.

Treat other options as needing a restart. Changed logging defaults apply only to **new** containers.

## Restart with minimum disruption
```bash
grep -q '"live-restore": true' /etc/docker/daemon.json && echo "live restore is enabled"
sudo systemctl restart docker
docker info --format '{{.LoggingDriver}} {{.Driver}} {{.DockerRootDir}}'
```
Live restore is meant to reduce container downtime during daemon restarts and upgrades.

## When dockerd will not start
```bash
sudo systemctl status docker --no-pager
sudo journalctl -u docker -b --no-pager | tail -30
```
Documented error: `the following directives are specified both as a flag and in the
configuration file: hosts`. With systemd the unit passes `-H`, so either remove the `hosts` key
from `daemon.json` or override `ExecStart=` in a drop-in to drop the `-H` argument (for example
`ExecStart=` then `ExecStart=/usr/bin/dockerd`).

## Gotchas
- Docker Desktop: the file is `$HOME/.docker/daemon.json`; edit it in the Docker Desktop Dashboard
  (Settings, Docker Engine) or a text editor.
- Rootless mode reads `~/.config/docker/daemon.json`; the regular Linux path is
  `/etc/docker/daemon.json`.

## Checked

Date: 2026-10-24. Documentation release: dockerd reference, daemon troubleshooting and Docker Desktop settings pages (docker/cli and docker/docs main).
Confirmed: the `--validate` flag, SIGHUP reload behaviour and the reloadable option list (including
`authorization-plugin` and `default-stop-timeout`), conflicting flag and file behaviour, the documented `hosts`
conflict error and systemd `ExecStart=` override, `daemon.json` locations for Linux, rootless and Docker
Desktop. Corrected: reload option names (`authorization-plugin`, not `authorization-plugins`), and removed `builder`
and `default-shm-size` which the reference does not list as reloadable. Removed: the `systemctl reload` form, the
generic JSON error strings, the `jq` check and the debug-run advice, none covered by the pages.

Method: documentation only; no commands were run.
