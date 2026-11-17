---
id: computing-software.cloud-infrastructure-engineering.docker.upgrading-containerd-io-with-docker-ce
name: upgrading-containerd-io-with-docker-ce
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, engine-upgrade, containerd-io-upgrade, containerd, live-restore, apt-mark-hold, runc]
level: advanced
status: docs-checked
description: "Upgrade the containerd.io package (containerd + runc) that Docker depends on: holding versions together, effect on running containers, live-restore, and verifying shims."
sources: ["https://docs.docker.com/engine/install/ubuntu/", "https://docs.docker.com/engine/daemon/live-restore/", "https://docs.docker.com/reference/api/engine/", "https://manpages.debian.org/bookworm/apt/apt-mark.8.en.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading containerd.io alongside docker-ce

Docker Engine runs containers through `containerd` and `runc`, shipped together in Docker's
`containerd.io` package. It is a separate package from `docker-ce`, so it must be upgraded and held alongside it.

## Hold and upgrade as a set
```bash
# Debian/Ubuntu
sudo apt-mark hold docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt list --all-versions containerd.io docker-ce
sudo apt-mark unhold containerd.io docker-ce docker-ce-cli
sudo apt-get install -y containerd.io=<ver> docker-ce=5:<ver> docker-ce-cli=5:<ver>
sudo apt-mark hold containerd.io docker-ce docker-ce-cli
# RHEL (dnf versionlock plugin installed)
sudo dnf versionlock add containerd.io docker-ce docker-ce-cli
```
Keep the packages held so they are upgraded only in a planned window.

## What happens to running containers
- Restarting `dockerd` stops containers unless `live-restore` is enabled in `daemon.json`; with it on, containers keep running while the daemon is unavailable (patch releases only).
- Docker's documentation does not describe what a `containerd.io` package upgrade does to running containers, so test on a canary host and plan a window.

## Procedure
```bash
docker info -f '{{.LiveRestoreEnabled}}'
containerd --version; runc --version
sudo apt-get install -y containerd.io=<ver>
sudo systemctl status containerd --no-pager
docker ps                                       # confirm containers are still running
docker compose up -d --force-recreate           # recreate a project's containers during the window if needed
```

## Verify
```bash
docker info -f '{{.ContainerdCommit.ID}} {{.RuncCommit.ID}}'
journalctl -u containerd --since -10m
```

## Gotchas
- Distro packages named `containerd` or `runc` conflict with `containerd.io`, which bundles both; remove them before installing Docker's packages.
- Test rollback on a canary host before relying on it.

## Checked

Checked against docker/docs `engine/install/ubuntu.md` (conflicting `containerd`/`runc` packages, `containerd.io` bundle), `engine/daemon/live-restore.md`, the Engine API swagger (`LiveRestoreEnabled`, `ContainerdCommit`, `RuncCommit`), the Compose `docker compose up` reference (`--force-recreate`), the Debian apt-mark manual and the dnf versionlock plugin docs (docker/docs latest commit 2026-10-23, Engine 29).

- `containerd.io` bundles containerd and runc; `apt-mark hold`/`unhold`; `dnf versionlock add`; `docker info` fields; `--force-recreate`.
- Removed as unconfirmed: the claim that containerd restarts never kill containers, the shim-survival and old-runc-in-memory statements, the Kubernetes note and the downgrade-state claim.

Method: documentation only; no commands were run.
