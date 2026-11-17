---
id: computing-software.cloud-infrastructure-engineering.docker.podman-docker-compatibility-and-quadlet
name: podman-docker-compatibility-and-quadlet
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, podman, podman-compat, podman-socket, quadlet, systemd, rootless, docker-compose]
level: practitioner
description: "Run Docker workflows on Podman: the Docker-compatible API socket for docker compose and SDKs, and Quadlet units for systemd-managed containers."
sources: ["https://docs.podman.io/en/latest/markdown/podman-system-service.1.html", "https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html", "https://podman.io/docs/installation"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Podman Docker compatibility and Quadlet

## Docker API socket (for docker compose, SDKs)
`podman system service` answers API calls on Linux and is usually run from systemd with socket activation. Its REST
API has a Docker-compatible layer (Docker v1.40 API) and a Podman-native Libpod layer. Unit files shipped by Podman:
- rootless: `/usr/lib/systemd/user/podman.service` and `podman.socket`, listening on `%t/podman/podman.sock`
  (`%t` expands to `$XDG_RUNTIME_DIR`);
- rootful: `/usr/lib/systemd/system/podman.service` and `podman.socket`, on `/run/podman/podman.sock`.
```sh
systemctl --user enable --now podman.socket           # rootless
export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock
```
Point Docker clients (docker CLI, compose, SDKs) at that socket with `DOCKER_HOST`. The command is not available when
Podman runs directly on a Windows or macOS host.

## Quadlet: containers as systemd units
Quadlet files are read by a systemd generator at boot and on `systemctl daemon-reload`, which generates the service
units. Search paths include `/etc/containers/systemd/` (rootful) and `~/.config/containers/systemd/` or
`$XDG_CONFIG_HOME/containers/systemd/` (rootless); `/etc/containers/systemd/users/` applies to users' sessions.
```ini
# ~/.config/containers/systemd/web.container
[Unit]
Description=Web
[Container]
Image=docker.io/library/nginx:<TAG>
PublishPort=8080:80
Volume=web-data.volume:/usr/share/nginx/html
AutoUpdate=registry
HealthCmd=/usr/bin/<HEALTH_COMMAND>
[Service]
Restart=always
[Install]
WantedBy=default.target
```
- Unit types: `.container`, `.volume`, `.network`, `.pod`, `.kube`, `.build`, `.image` and `.artifact`.
- `AutoUpdate=registry` is the same as the `io.containers.autoupdate=registry` label.
- `HealthCmd=` equals `--health-cmd`.
- The generator applies the `[Install]` section itself, as `systemctl enable` would.
- A container whose image name ends in `.build` uses the image from that `.build` file and depends on
  `<name>-build.service`.

## Verify
After `systemctl --user daemon-reload`, the generated `web.service` appears in `systemctl --user status web`.

## Checked
2026-10-28. Confirmed on `podman-system-service(1)` (compat vs Libpod layers, socket and unit file paths, Windows/macOS
limitation) and `podman-systemd.unit(5)` (search paths, unit types, keys, generator behaviour, `.build` dependency).
Removed (not in the fetched pages): `podman-docker` package and alias, short-name registry config, rootless port and
`:U`/`:Z` volume advice, `--restart` behaviour, `podman compose`, Testcontainers variables, `podman auto-update`,
`loginctl enable-linger`, the `podman generate systemd` deprecation, and the `docker version` check.
Method: documentation only; no commands were run.
