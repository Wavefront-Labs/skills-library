---
id: computing-software.systems-network-administration.linux.systemd-user-units-and-lingering
name: systemd-user-units-and-lingering
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, user-units, systemd-user, systemctl-user, loginctl-enable-linger, linger, xdg-runtime-dir, rootless-services, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Run services as an unprivileged user with systemd --user: unit locations, systemctl --user over ssh/su, lingering so they survive logout and start at boot, and journal access."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  - https://www.freedesktop.org/software/systemd/man/latest/loginctl.html
  - https://www.freedesktop.org/software/systemd/man/latest/user@.service.html
  - https://docs.kernel.org/networking/ip-sysctl.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Per-user systemd units

**Goal:** a non-root service account runs its own long-lived services and timers, managed
with `systemctl --user`, started at boot without anyone logging in.

## 1. Where units go
| Path | Scope |
|---|---|
| `~/.config/systemd/user/` | this user only (what you normally write) |
| `/etc/systemd/user/` | admin-provided for all users |
| `/usr/lib/systemd/user/` | packages |
```ini
# ~/.config/systemd/user/worker.service
[Unit]
Description=Queue worker
[Service]
ExecStart=%h/bin/worker --queue jobs
Restart=on-failure
[Install]
WantedBy=default.target
```
```bash
systemctl --user daemon-reload
systemctl --user enable --now worker.service
journalctl --user -u worker -f
```

## 2. Survive logout and start at boot: lingering
With lingering enabled a user manager is spawned at boot and kept around after logouts, so a user who is not logged in can run long-running services.
```bash
loginctl enable-linger svc-app
loginctl show-user svc-app -p Linger
```

## 3. Managing as root / from sudo
Reach a user's manager from root with `--machine` (systemd 248 and later), or open a session as that user:
```bash
systemctl --user -M svc-app@ status worker
machinectl shell svc-app@ /bin/bash
```

## 4. Limits and differences
- Sandboxing settings that need file system namespacing (such as `ProtectSystem=`) are not available in user services unless combined with `PrivateUsers=true` (`systemd.exec`).
- Binding ports below 1024 as an unprivileged user depends on the `net.ipv4.ip_unprivileged_port_start` sysctl.
- The user's `user-UID.slice` carries `TasksMax=33%` from systemd's default `user-.slice.d` drop-in, capping everything the user runs.

## Gotchas
- `enable` without lingering looks fine, but the user manager stops after the last session ends.

## Verify
- [ ] `loginctl show-user <user> -p Linger` is `yes`.
- [ ] Reboot, don't log in: `systemctl --user -M <user>@ is-active worker` reports active.
- [ ] `journalctl --user -u worker` (as the user) shows its logs.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: user unit search path (`~/.config/systemd/user`, `/etc/systemd/user`, `/usr/lib/systemd/user`); `loginctl enable-linger` semantics; `systemctl --user -M user@` (v248 NEWS); `machinectl shell` takes `NAME@`; user services cannot use file-system-namespacing settings without `PrivateUsers=`; `ip_unprivileged_port_start` (kernel ip-sysctl); `user-.slice.d/10-defaults.conf` sets `TasksMax=33%`. Removed the logind `UserTasksMax=` claim (no longer in the logind.conf documentation), the Podman, NFS-home and su remarks and the `/var/lib/systemd/linger` listing.

Method: documentation only; no commands were run.
