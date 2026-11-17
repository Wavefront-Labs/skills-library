---
id: computing-software.cloud-infrastructure-engineering.docker.dockerd-daemon-json-systemd-overrides-and-debug-logs
name: dockerd-daemon-json-systemd-overrides-and-debug-logs
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, daemon-json, dockerd, daemon-config, data-root, daemon-json-options, dockerd-systemd-override, execstart-conflict, dockerd-debug, daemon-logs]
level: advanced
description: "Set the daemon.json options that matter (data-root, log-opts, address pools, live-restore), avoid the -H vs hosts conflict in systemd overrides, and debug dockerd."
sources: ["https://docs.docker.com/reference/cli/dockerd/#daemon-configuration-file", "https://docs.docker.com/engine/daemon/", "https://docs.docker.com/engine/daemon/troubleshoot/", "https://docs.docker.com/engine/daemon/logs/", "https://github.com/moby/moby/blob/master/contrib/init/systemd/docker.service"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# daemon.json, systemd overrides and dockerd debugging

## A sane production daemon.json
```json
{
  "data-root": "/srv/docker",
  "log-driver": "json-file",
  "log-opts": { "max-size": "20m", "max-file": "5" },
  "live-restore": true,
  "default-address-pools": [{ "base": "172.30.0.0/16", "size": 24 }],
  "bip": "172.29.0.1/24",
  "userland-proxy": false,
  "no-new-privileges": true,
  "icc": false,
  "features": { "containerd-snapshotter": true },
  "metrics-addr": "127.0.0.1:9323"
}
```
Linux path `/etc/docker/daemon.json`; rootless `~/.config/docker/daemon.json`. Validate before
restarting: `dockerd --validate --config-file /etc/docker/daemon.json`.
Reloadable without restart (SIGHUP; the packaged unit's ExecReload sends it): `debug`, `labels`,
`live-restore`, `max-concurrent-downloads`, `max-concurrent-uploads`, `max-download-attempts`, `default-runtime`, `default-stop-timeout`, `runtimes`, `authorization-plugin`, `insecure-registries`, `registry-mirrors`, `shutdown-timeout` and `features`. Everything else needs a restart. The daemon still rejects a reload that conflicts with CLI flags.

## The hosts conflict
```
unable to configure the Docker daemon with file /etc/docker/daemon.json:
the following directives are specified both as a flag and in the configuration file: hosts
```
The packaged unit runs `dockerd -H fd:// --containerd=/run/containerd/containerd.sock`. Setting `"hosts"` in daemon.json
conflicts. Fix with a drop-in that clears ExecStart:
```ini
# systemctl edit docker  ->  /etc/systemd/system/docker.service.d/override.conf
[Service]
ExecStart=
ExecStart=/usr/bin/dockerd --containerd=/run/containerd/containerd.sock
```
The empty `ExecStart=` is required; without it systemd errors with "more than one ExecStart".
Then `systemctl daemon-reload && systemctl restart docker`. Same rule for any flag also in
daemon.json - pick one place (daemon.json).

Other drop-in use: `Environment="HTTP_PROXY=..."` (or daemon.json `proxies`; see the proxy skill).

## Debugging the daemon
```sh
journalctl -u docker -b --no-pager | tail -100
journalctl -u docker -f
# enable debug without restart: set "debug": true in daemon.json, then reload
sudo kill -SIGHUP $(pidof dockerd)
# goroutine dump for hangs
sudo kill -SIGUSR1 $(pidof dockerd)   # writes goroutine-stacks-*.log under /var/run/docker; the daemon keeps running
# alternative: stop the service and start dockerd manually with -D
sudo systemctl stop docker && sudo dockerd -D
```
Also check containerd: `journalctl -u containerd`.

## Verify
`docker info` reflects the new `Docker Root Dir`, logging driver and live-restore;
`systemctl cat docker` shows your override in effect. If `log-level` is set it must be one of `debug`, `info` (default), `warn`, `error`, `fatal`.

## Checked

Checked against docker/docs `engine/daemon/_index.md`, `daemon/logs.md`, `daemon/troubleshoot.md`, the dockerd reference (`reference/cli/dockerd`) and moby `contrib/init/systemd/docker.service` (docker/docs latest commit 2026-10-23, Engine 29).

- daemon.json keys in the example (`data-root`, `log-driver`, `log-opts`, `live-restore`, `default-address-pools`, `bip`, `userland-proxy`, `no-new-privileges`, `icc`, `features`) appear in the dockerd reference; `--metrics-addr` serves the metrics API (example `127.0.0.1:9323`). `containerd-snapshotter` is now the default for fresh installs in Engine 29, so the example sets it explicitly.
- The reloadable-options table, SIGHUP reload, the `hosts` flag conflict error, the empty `ExecStart=` fix, SIGUSR1 stack dump location and `journalctl -u docker.service` all match the documentation.
- Removed as unconfirmed: the "Engine 23+" gate, the jq edit pipeline, `docker info` debug grep, and the systemd mount-dependency suggestions.

Method: documentation only; no commands were run.
