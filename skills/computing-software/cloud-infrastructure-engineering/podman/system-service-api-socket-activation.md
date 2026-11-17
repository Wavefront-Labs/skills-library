---
id: computing-software.cloud-infrastructure-engineering.podman.system-service-api-socket-activation
name: system-service-api-socket-activation
category: computing-software
field: cloud-infrastructure-engineering
product: podman
tags: [system-service, rest-api, socket-activation, podman-socket, docker-host, linger, systemd]
level: practitioner
status: docs-checked
description: "Provide the Podman REST API on demand with podman system service and systemd socket activation: rootful and rootless sockets, idle --time, DOCKER_HOST and linger."
sources:
  - https://docs.podman.io/en/latest/markdown/podman-system-service.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: expose a Docker-compatible and Libpod API with minimal idle cost.

`podman system service` creates a listening service for API calls. It is Linux only, usually run from systemd, and unavailable on Windows or macOS hosts or when using a remote Podman. The REST API has a Docker v1.40 compatibility layer and a native Libpod layer. Both are versioned but the server does not reject unsupported versions.

With systemd socket activation the service starts when a client connects and, after the `--time` idle period (default 5 seconds; `0` means no timeout), exits, leaving `podman.service` inactive until the next connection. User units are `/usr/lib/systemd/user/podman.service` and `podman.socket`, with `ListenStream=%t/podman/podman.sock` where `%t` expands to `XDG_RUNTIME_DIR`. Rootful units live in `/usr/lib/systemd/system/` with socket `/run/podman/podman.sock`. Only one listening socket is supported.

Commands: `systemctl --user start podman.socket`; `systemctl --user enable podman.socket` with `loginctl enable-linger <USER>` for after reboots; `sudo systemctl start podman.socket` and `sudo systemctl enable podman.socket` for rootful.

Docker tools: `export DOCKER_HOST=unix://$XDG_RUNTIME_DIR/podman/podman.sock` then `docker-compose up`.

Direct run: `podman system service --time 0 unix:///var/run/mypodman.sock` listens on a custom socket indefinitely. Without socket activation the API is not available on demand after the idle timeout. Default endpoints: `unix:///run/podman/podman.sock` (rootful) or `unix://$XDG_RUNTIME_DIR/podman/podman.sock`. The default systemd units set log level to `info` rather than `error`.

## Checked
2026-11-09: read the podman-system-service man page in full and confirmed the platform limits, API layers, socket activation behaviour, --time default, unit file paths, socket paths, one-socket limit, example commands, DOCKER_HOST export and the log level note. Nothing removed; every claim was confirmed.

Method: documentation only; no commands were run.

