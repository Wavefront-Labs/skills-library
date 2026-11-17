---
id: computing-software.cloud-infrastructure-engineering.docker.compose-under-systemd-units
name: compose-under-systemd-units
category: computing-software
field: cloud-infrastructure-engineering
product: docker
tags: [docker, compose, docker-compose, systemd-compose, systemd, unit-file, restart-policy, live-restore, daemon-reload, systemctl, boot-persistence, process-supervision, single-host-deploy, compose-production]
level: practitioner
status: gated
description: "Run docker compose as a systemd service: the unit pattern with up --wait and Restart, restart policies versus live-restore across daemon restarts, and reload instead of restart."
sources: ["https://docs.docker.com/engine/daemon/live-restore/", "https://docs.docker.com/reference/cli/docker/compose/up/", "https://docs.docker.com/engine/daemon/live-restore/", "https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compose under systemd units

**Goal:** Compose services survive reboots and daemon restarts on a single Linux host, under one
process supervisor, without two layers of supervision fighting each other.

Docker's daemon is itself a systemd service; adding one unit per Compose project puts the whole
stack under the same supervisor, with boot ordering and logs in `journalctl`.

## The unit pattern
```ini
# /etc/systemd/system/compose-app.service
[Unit]
Description=Compose app
Requires=docker.service
After=docker.service network-online.target

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/app
ExecStart=/usr/bin/docker compose up -d --wait --remove-orphans
ExecStop=/usr/bin/docker compose down
ExecReload=/usr/bin/docker compose up -d --wait --remove-orphans
TimeoutStartSec=300

[Install]
WantedBy=multi-user.target
```
```bash
systemctl daemon-reload
systemctl enable --now compose-app.service
systemctl status compose-app        # journalctl -u compose-app -f for logs
```

`--wait` is the load-bearing flag: it "waits for services to be running|healthy", so the unit only
reports started once healthchecks pass - `--wait-timeout` bounds it. `Type=oneshot` with
`RemainAfterExit=yes` treats the stack as a started resource rather than a foreground process.
`ExecReload` makes `systemctl reload compose-app` re-apply the Compose file (new containers) without
a stop/start.

The unit-file shape is convention, not a Docker-documented interface - Docker documents the daemon
side (below), and the Compose CLI flags; check the unit against your systemd's `systemd.service`
manual for the directives.

## Daemon restarts: live-restore, not just the unit
By default the daemon shuts down all containers when it stops. **Live restore** keeps containers
running across a daemon shutdown or restart:

```json
{ "live-restore": true }
```
in `/etc/docker/daemon.json` (Docker Desktop: Settings -> Docker Engine). Then, instead of a full
restart, reload the daemon without container downtime: `systemctl reload docker` (or `SIGHUP` to
`dockerd`). Starting `dockerd --live-restore` by hand is explicitly **not recommended** - it skips
the environment a process manager sets up.

Limits worth knowing:
- Live restore applies to **standalone containers only** - not Swarm services.
- It survives daemon updates across **patch releases only** (`YY.MM.x`), not major upgrades, and
  not if daemon options (bridge IPs, graph driver) changed - the daemon can then fail to reattach
  and the containers must be stopped manually.
- A long daemon outage can fill the 64K FIFO log buffer, which **blocks containers from logging**
  until the daemon restarts; the kernel limit can be raised via `/proc/sys/fs/pipe-max-size` on
  Linux (not on Docker Desktop).
- Not supported for Windows containers.

## Who restarts what
Two supervisors are in play: systemd restarts the *unit* (the `docker compose` invocation, and
ultimately the containers via `Restart=` on the unit); the daemon's restart policies restart
*containers* when they exit. Decide once: either let the unit own lifecycle (`Restart=on-failure`
on the service, `restart: unless-stopped` in Compose for crash-restarts) or let Compose own it
entirely and keep the unit `Type=oneshot` purely for boot ordering. Doubling up means a crash gets
restarted by whichever wins the race, which makes flapping hard to reason about.

## Failure modes
- **Containers die on every reboot** - no unit (or no `enable`), and the Compose `restart:` policy
  alone cannot start containers before the daemon exists at boot.
- **Unit claims started while the app is broken** - no `--wait`, so `up -d` returning counts as
  success; healthchecks never checked.
- **Containers stop when the daemon upgrades** - live-restore across a major release, or daemon
  options changed under it.
- **Logs freeze during a daemon outage** - the 64K FIFO filled.
- **Restart loops that never converge** - systemd `Restart` and Compose `restart:` both active with
  different backoff expectations.
- **Two Compose stacks fight over the same name** - running `docker compose up` by hand while the
  unit also manages the project: let one path own it.

## Verify
- [ ] `systemctl enable --now` brings the whole stack up from a reboot, in dependency order after
      `docker.service`.
- [ ] `systemctl status` reports started only once healthchecks pass (`--wait`), and
      `--wait-timeout` bounds the worst case.
- [ ] `systemctl reload docker` (with live-restore) restarts the daemon with zero container
      downtime - verify with a continuous request stream.
- [ ] `systemctl reload compose-app` applies a changed Compose file without a full stop.
- [ ] Exactly one of systemd `Restart` / Compose `restart:` owns crash-restarts, and that choice is
      written down.

*`--wait`/`--wait-timeout`/`-d` semantics from the Compose CLI reference, and live-restore
behaviour, platform limits and the 64K buffer from the official live-restore page, both checked
2026-11-01. The unit-file pattern itself is community convention, not Docker-documented. Nothing was
executed, so `status: draft`.*

## Checked

- Date: 2026-11-02.
- Confirmed against: docker compose up --wait and --remove-orphans (Docker docs); systemd.service ExecStart, ExecStop, ExecReload, RemainAfterExit, TimeoutStartSec (systemd.service man page); live-restore daemon option.
- Not confirmed: the unit file layout and docker.service dependency wording beyond the man page (gated: unconfirmed, source is paywalled or blocked). Treat as unverified and check the current vendor documentation.

Method: documentation only; no commands were run.
