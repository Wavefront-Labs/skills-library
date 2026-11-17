---
id: computing-software.cloud-infrastructure-engineering.docker.daemon-hardening-settings
name: daemon-hardening-settings
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, hardening, daemon-hardening, daemon-json, cis-daemon-configuration, no-new-privileges, icc]
level: advanced
status: docs-checked
description: "A hardened daemon.json baseline mapped to CIS Docker daemon checks: icc, no-new-privileges, userland-proxy, live-restore, logging, ulimits, userns-remap, bind IP."
sources: ["https://docs.docker.com/reference/cli/dockerd/", "https://docs.docker.com/engine/daemon/live-restore/", "https://docs.docker.com/engine/logging/drivers/local/", "https://docs.docker.com/engine/security/protect-access/", "https://github.com/docker/docker-bench-security"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Daemon hardening settings

## Baseline daemon.json
```json
{
  "icc": false,
  "no-new-privileges": true,
  "userland-proxy": false,
  "live-restore": true,
  "log-driver": "local",
  "log-opts": { "max-size": "20m", "max-file": "5" },
  "default-ulimits": { "nofile": { "Name": "nofile", "Soft": 65536, "Hard": 65536 } },
  "userns-remap": "default",
  "ip": "127.0.0.1",
  "default-address-pools": [{ "base": "172.30.0.0/16", "size": 24 }],
  "experimental": false
}
```
Validate and apply: `sudo dockerd --validate --config-file /etc/docker/daemon.json && sudo systemctl restart docker`.

## What each does (and the catch)
| Key | Effect | Catch |
|---|---|---|
| `icc: false` | Blocks container-to-container traffic on the **default bridge** | User-defined networks are unaffected; segment those with separate networks |
| `no-new-privileges: true` | Default for all containers: setuid binaries cannot gain privileges | Breaks images relying on `sudo`/`su`/setuid at runtime |
| `userland-proxy: false` | The userland proxy (used for loopback traffic) is not started | Loopback-to-published-port behaviour then relies on the firewall rules |
| `live-restore: true` | Containers keep running while the daemon is down | Applies to standalone containers, not Swarm services |
| `log-driver` + rotation | Prevents disks filling (`local` defaults: 20m x 5 files, compressed) | The `local` files are for the daemon only; external tools should not read them |
| `default-ulimits` | Sane nofile defaults | Some DBs need higher per container |
| `userns-remap` | Container root is unprivileged on host | Existing images are masked; `--privileged`, `--pid=host` and `--network=host` need `--userns=host` |
| `ip: 127.0.0.1` | Default host IP for port publishing from the default bridge network (default `0.0.0.0`) | Public services must publish `0.0.0.0:` explicitly; user-defined networks are not covered |

## Also part of the daemon section of CIS
- No TCP socket without TLS (`tlsverify` + certs) if remote access is needed.
- Authorization plugin where the daemon is shared.
- Keep seccomp default profile; do not set `"seccomp-profile": "unconfined"`.
- Restrict `insecure-registries` to none.
- Check the current CIS Docker Benchmark for the full daemon and host lists (the benchmark text is not
  reproduced here).

## Verify
```bash
docker info --format '{{json .SecurityOptions}} live={{.LiveRestoreEnabled}} log={{.LoggingDriver}}'
docker run --rm alpine grep NoNewPrivs /proc/self/status     # NoNewPrivs: 1
docker run --rm -d -p 8080:80 nginx && ss -tlnp | grep 8080  # 127.0.0.1:8080
```
Run Docker Bench for Security afterwards (clone `docker/docker-bench-security` and build or run it per its
README; the README notes the published `docker/docker-bench-security` image is out of date) to review the
daemon section.

## Checked
Date: 2026-10-24. Documentation: Docker docs (docker/docs main: `dockerd` reference, live-restore, local logging driver pages), docker/docker-bench-security README, Docker Engine API (LiveRestoreEnabled, LoggingDriver, SecurityOptions).
- Confirmed daemon.json keys and meanings: `icc` (default bridge only, default true), `no-new-privileges`, `userland-proxy` (loopback traffic), `live-restore`, `ip` (default bridge, default 0.0.0.0), `default-ulimits` (Name/Hard/Soft), `default-address-pools`, `experimental`, `userns-remap`, `log-driver`/`log-opts`, and `dockerd --validate --config-file`.
- Confirmed `local` driver defaults (max-size 20m, max-file 5, compression on) and its warning about external tools, live-restore applying only to standalone containers, and the `docker info` fields used in Verify.
- Removed the CIS audit-rule bullet detail and the Swarm incompatibility statement, replaced with documented behaviour; noted the Docker Bench image is out of date.
Method: documentation only; no commands were run.
