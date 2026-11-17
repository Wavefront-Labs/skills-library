---
id: computing-software.cloud-infrastructure-engineering.docker.upgrading-docker-engine-with-live-restore-and-rollback
name: upgrading-docker-engine-with-live-restore-and-rollback
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, engine-upgrade, docker-upgrade, live-restore, live-restore-daemon-json, live-restore-limits, apt-mark-hold, version-hold, engine-rollback, engine-downgrade]
level: advanced
description: "Upgrade docker-ce in a controlled way: hold package versions, use live-restore to keep containers running across daemon restarts, know its limits, and roll back."
sources: ["https://docs.docker.com/engine/daemon/live-restore/", "https://docs.docker.com/engine/install/ubuntu/", "https://docs.docker.com/engine/install/rhel/", "https://docs.docker.com/engine/deprecated/", "https://manpages.debian.org/bookworm/apt/apt-mark.8.en.html"]
status: docs-checked
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Upgrading Docker Engine with live-restore and rollback

## Hold versions so upgrades are deliberate
```sh
sudo apt-mark hold docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
apt-mark showhold
# RHEL: with the dnf versionlock plugin installed: dnf versionlock add docker-ce docker-ce-cli containerd.io
```
`apt-mark hold` stops a package being automatically installed, upgraded or removed; `dnf versionlock` excludes other versions. Docker warns that unplanned installs can bring unexpected major upgrades, so make upgrades deliberate.

## live-restore
```json
{ "live-restore": true }
```
On Linux, `systemctl reload docker` (or SIGHUP to `dockerd`) applies it without a restart. By default containers stop when the daemon stops; with live-restore they stay running while the daemon is unavailable.

Limits:
- Supported only for patch releases (`YY.MM.x`), not major (`YY.MM`) daemon upgrades. If you skip releases the daemon may not reconnect to the containers and you must stop them manually.
- It works only if daemon options such as bridge IP addresses and the graph driver did not change.
- It applies to standalone containers, not Swarm services; it is not supported for Windows containers.
- While dockerd is down, containers keep writing to a FIFO log buffer (default 64K); once full, they block on logging and you must restart the daemon to flush it. On Linux the size follows `/proc/sys/fs/pipe-max-size`.
- Keep the downtime short.

## Upgrade runbook
1. Read release notes and the deprecated features page for breaking changes.
2. Back up `/etc/docker`, note `docker version`, `docker info`.
3. Drain if you can (move traffic away / Swarm `node update --availability drain`).
4. `sudo apt-mark unhold docker-ce docker-ce-cli && sudo apt-get install docker-ce=<ver> docker-ce-cli=<ver>`; re-hold.
5. Check `docker info`, `docker ps`, a test container on each network type, published ports.

## Rollback
```sh
apt list --all-versions docker-ce
sudo apt-get install --allow-downgrades docker-ce=<old> docker-ce-cli=<old> containerd.io=<old>
sudo systemctl restart docker
```
- Take a copy of `/var/lib/docker` with Docker stopped before upgrading so you have a restore point.
- Docker's documentation gives no downgrade guarantees; test the rollback path on a staging host before relying on it.

## Verify
`docker version` shows the target; with live-restore,
`docker inspect -f '{{.State.StartedAt}}' <ctr>` is unchanged across the daemon restart.

## Checked

Checked against docker/docs `engine/daemon/live-restore.md`, `engine/install/ubuntu.md`, `engine/install/rhel.md` and the Deprecated Engine Features page (docker/docs latest commit 2026-10-23, Engine 29); apt-mark behaviour against the Debian apt-mark manual and `versionlock` against the dnf-plugins-core documentation.

- Live-restore: `{"live-restore": true}`, reload with `systemctl reload docker` or SIGHUP, patch-release-only upgrades, unchanged daemon options, FIFO log buffer 64K, standalone containers only, no Windows containers.
- `apt-mark hold`, `unhold` and `showhold`; `dnf versionlock add`; `apt list --all-versions docker-ce` for versions.
- Removed as unconfirmed: statements about containerd restarts killing containers, userland-proxy and DNS behaviour during daemon downtime, the Swarm "ignored" wording, and major-version downgrade failure claims.

Method: documentation only; no commands were run.
