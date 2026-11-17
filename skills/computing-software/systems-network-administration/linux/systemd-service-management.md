---
id: computing-software.systems-network-administration.linux.systemd-service-management
name: systemd-service-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, systemctl, journalctl, unit-file, service, daemon, daemon-reload, drop-in, systemctl-edit, restart-policy, restartsec, startlimitburst, systemd-timer, cron, sandboxing, hardening, protectsystem, dynamicuser, systemd-analyze, sysadmin, init-system, service-type]
level: practitioner
status: docs-checked
description: "Run Linux services with systemd: unit files, restart policies, hardening, drop-ins, timers vs cron, and journalctl."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.service.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.exec.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.timer.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# systemd service management — units that restart, log and stay contained

**Goal:** turn any long-running program into a supervised, hardened, logged service,
and change it safely.

## 1. A sane unit file
Put your own units in `/etc/systemd/system/` (never edit files under `/usr/lib/systemd/`;
package upgrades overwrite them).

```ini
# /etc/systemd/system/myapp.service
[Unit]
Description=My app
Wants=network-online.target
After=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=5

[Service]
Type=simple            # use notify if the app calls sd_notify; exec to catch exec failures
User=myapp
WorkingDirectory=/opt/myapp
EnvironmentFile=-/etc/myapp/env
ExecStart=/opt/myapp/bin/myapp --port 8080
Restart=on-failure
RestartSec=5s
TimeoutStopSec=30s

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now myapp
systemctl status myapp
```

Gotchas:
- **`daemon-reload` after every unit edit.** Without it systemd keeps the old definition
  and `status` warns "unit file changed on disk".
- `StartLimitIntervalSec=` and `StartLimitBurst=` belong in `[Unit]`. With the example
  values, a sixth start within 300 s is refused (result `start-limit-hit`) until
  `systemctl reset-failed myapp`.
- `After=network.target` does not mean "network is up". Use `network-online.target`
  and pair it with `Wants=`.
- `ExecStart` is not a shell: no pipes, `>` or `&&`. Wrap in `/bin/sh -c '...'` or a script.

## 2. Change units with drop-ins, not copies
```bash
sudo systemctl edit myapp          # creates /etc/systemd/system/myapp.service.d/override.conf
sudo systemctl edit --full myapp   # full copy; avoid, it stops tracking vendor changes
systemctl cat myapp                # shows the merged result, file by file
```
To *replace* a list setting such as `ExecStart`, clear it first in the drop-in:
`ExecStart=` then `ExecStart=/new/command`. `systemctl edit` reloads for you.

## 3. Hardening directives (add, then test)
```ini
NoNewPrivileges=yes
ProtectSystem=strict        # whole file system read-only except /dev, /proc, /sys; allow paths with ReadWritePaths=
ReadWritePaths=/var/lib/myapp
ProtectHome=yes
PrivateTmp=yes
PrivateDevices=yes
ProtectKernelTunables=yes
ProtectControlGroups=yes
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
CapabilityBoundingSet=CAP_NET_BIND_SERVICE   # only the listed capabilities stay in the bounding set
```
`systemd-analyze security myapp` scores exposure (lower is better). Add directives one
or two at a time: a too-tight `ProtectSystem=strict` shows up as EROFS / permission
errors in the journal. `DynamicUser=yes` is handy for stateless services; pair it with
`StateDirectory=myapp`.

## 4. Logs with journalctl
```bash
journalctl -u myapp -f                 # follow
journalctl -u myapp -b -p warning      # this boot, warning and worse
journalctl -u myapp --since "1 hour ago" -o short-iso
systemctl list-units --failed
```
If logs vanish at reboot, the journal is volatile: create `/var/log/journal` or set
`Storage=persistent` in `journald.conf`, and cap it with `SystemMaxUse=` (for example 1G).

## 5. Timers vs cron
```ini
# backup.timer  (pairs with backup.service, Type=oneshot)
[Timer]
OnCalendar=*-*-* 02:30:00
RandomizedDelaySec=15m
Persistent=true            # run on boot if the machine was off at 02:30
[Install]
WantedBy=timers.target
```
`systemctl enable --now backup.timer`; `systemctl list-timers` shows next/last run.
Timers win over cron for logging (journal), no overlap (a running oneshot is not
restarted), dependencies and catch-up. Check expressions with
`systemd-analyze calendar "*-*-* 02:30"`. Cron is still fine for user-level jobs.

## 6. Which service uses the resources
`systemd-cgtop` shows CPU, memory and I/O per control group; `-m` orders by memory.

## Verify
- [ ] `systemctl is-enabled myapp` says `enabled` and the service survives a reboot.
- [ ] `kill -9 <PID>` of the main process is followed by an automatic restart after `RestartSec`.
- [ ] `systemctl cat myapp` shows your drop-in, and no vendor unit was edited in place.
- [ ] `systemd-analyze security myapp` exposure dropped after hardening, and the app still works.
- [ ] `systemctl list-timers` shows the next run for every timer you created.
- [ ] Journal is persistent and size-capped.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `StartLimitIntervalSec=`/`StartLimitBurst=` in `[Unit]` and the `start-limit-hit` result; `Type=exec` recommended for long-running services; no shell syntax in `ExecStart=`; `ProtectSystem=strict` semantics; `CapabilityBoundingSet=` semantics; `DynamicUser=` with `StateDirectory=`; `Storage=auto` behaviour in `journald.conf`; `Persistent=` and `RandomizedDelaySec=`; a timer does not restart an already active unit; `systemctl edit` reloads configuration. The vmstat/iostat triage table was removed because no systemd documentation covers it.

Method: documentation only; no commands were run.
