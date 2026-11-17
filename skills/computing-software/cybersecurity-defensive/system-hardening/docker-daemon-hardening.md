---
id: computing-software.cybersecurity-defensive.system-hardening.docker-daemon-hardening
name: docker-daemon-hardening
category: computing-software
field: cybersecurity-defensive
product: system-hardening
tags: [container-hardening, docker-daemon-hardening, daemon-json, userns-remap, docker-socket, live-restore, icc]
level: advanced
status: docs-checked
description: "Harden the Docker daemon: daemon.json settings (icc, userns-remap, no-new-privileges, logging), protect the Docker socket, TLS for remote API and audit rules."
sources: ["https://github.com/docker/cli/blob/master/docs/reference/dockerd.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/protect-access.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/security/userns-remap.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/network/packet-filtering-firewalls.md", "https://github.com/docker/docs/blob/main/content/manuals/engine/network/port-publishing.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Docker daemon hardening

**Goal:** the Docker host and daemon cannot be trivially abused for root access, and containers start with safe defaults.

## `/etc/docker/daemon.json`
```json
{
  "icc": false,
  "userns-remap": "default",
  "no-new-privileges": true,
  "live-restore": true,
  "userland-proxy": false,
  "log-driver": "json-file",
  "log-opts": { "max-size": "50m", "max-file": "5" },
  "default-ulimits": { "nofile": { "Name": "nofile", "Hard": 65536, "Soft": 32768 } },
  "experimental": false
}
```
- `icc: false` blocks inter-container traffic on the default bridge (use user-defined networks with explicit membership).
- `userns-remap` maps container root to an unprivileged host UID range. Documented limitations: sharing PID or network namespaces with the host (`--pid=host`, `--network=host`), volume or storage drivers that cannot use the daemon's mappings, and `--privileged` (unless `--userns=host` is also given) are incompatible; host volumes need their ownership arranged in advance.
- `"no-new-privileges": true` makes it the default for new containers; commands that raise privileges, such as `su` and `sudo`, no longer work inside them.
Restart the daemon with your init system; `docker info` lists the security options.

## The socket is root
- Anyone who can reach the daemon (including `docker` group members) effectively has root on the host. Limit access to admins; do not mount `/var/run/docker.sock` into containers (CI runners, monitoring) unless the exposure is accepted.
- Remote API only with TLS and client certificate verification: `"hosts": ["unix:///var/run/docker.sock","tcp://0.0.0.0:2376"], "tlsverify": true, "tlscacert": ..., "tlscert": ..., "tlskey": ...`. Docker's documentation says Docker over TLS should run on port 2376; never expose an unauthenticated TCP listener.
- Authorization plugins (`--authorization-plugin`) can extend access control on multi-user hosts.

## Host
- Dedicated container hosts, minimal OS, up-to-date kernel and Docker Engine.
- auditd rules for Docker files: `-w /usr/bin/dockerd -k docker`, `-w /var/lib/docker -k docker`, `-w /etc/docker -k docker`, `-w /usr/lib/systemd/system/docker.service -k docker`, `-w /var/run/docker.sock -k docker`.
- Separate partition for `/var/lib/docker`.

## Gotchas
- Published container ports are diverted before they reach the `INPUT` and `OUTPUT` chains that ufw uses, so ufw rules do not filter them; use the `DOCKER-USER` chain for your own filtering, or publish on the loopback address (`-p 127.0.0.1:8080:80`).
- With `userns-remap`, Docker stores images and containers in a separate subdirectory of `/var/lib/docker`, so existing ones are not visible; plan the migration.

## Verify
- [ ] `docker info --format '{{json .SecurityOptions}}'` reflects the security options in effect.
- [ ] `ss -tlpn | grep dockerd` shows no unauthenticated TCP listener (only 2376 with TLS, if remote access is needed).

## Checked
Checked 2026-10-25 against the Docker documentation sources (docker/cli `dockerd` reference, docker/docs protect-access, userns-remap, packet-filtering-firewalls and port-publishing pages, last commits 2026-10-23). Confirmed: every `daemon.json` key in the sample (icc, userns-remap, no-new-privileges, live-restore, userland-proxy, log-driver, log-opts, default-ulimits, experimental, hosts, tlsverify, tlscacert, tlscert, tlskey), `--icc` default true for the default bridge, the userns-remap limitations and storage behaviour, TLS on port 2376, `--authorization-plugin`, `docker info --format '{{json .SecurityOptions}}'`, ufw bypass and the `DOCKER-USER` chain, and publishing on 127.0.0.1. Removed unconfirmed: the cryptomining remark, OPA plugin name, docker-bench pass criterion, CIS Docker Benchmark reference (not read) and the claim that `.SecurityOptions` lists specific default entries. The auditd watch rules are generic auditd syntax (see auditd-rules) and were not tied to a Docker document.

Method: documentation only; no commands were run.
