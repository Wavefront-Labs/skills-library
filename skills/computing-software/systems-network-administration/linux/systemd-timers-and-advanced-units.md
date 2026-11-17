---
id: computing-software.systems-network-administration.linux.systemd-timers-and-advanced-units
name: systemd-timers-and-advanced-units
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, timer, templated-unit, instantiated-unit, socket-activation, oneshot, onfailure, wants, requires, bindsto, partof, ordering, dependency, sysadmin, oncalendar, persistent-timer, randomizeddelaysec]
level: advanced
status: docs-checked
description: "Advanced systemd unit features beyond a basic service: templated/instantiated units, socket activation, dependency vs ordering, and OnFailure handling."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.socket.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Advanced systemd units — templates, sockets, and getting ordering right

**Goal:** go past a single hand-written `.service` file (covered in
`computing-software.systems-network-administration.linux.systemd-service-management`)
into the features that let one unit file serve many instances, start on
demand instead of at boot, and fail loudly in the right direction — the
dependency/ordering distinction is the one that causes the most subtle bugs.

## 1. Dependency vs ordering — two separate axes, often confused
`Wants=`/`Requires=`/`BindsTo=` decide **whether** a unit starts; `After=`/
`Before=` decide **when**, relative to each other — neither implies the
other.
```ini
[Unit]
Wants=redis.service
After=redis.service
```
`Wants=redis.service` with no `After=` means systemd starts both in
parallel — the app can start *before* redis is listening, a classic race
that `systemctl status` won't show as an error because both units
"started successfully," just not in the order the app needed.
`Requires=` without `After=` is the same race but with a harder failure
mode (if redis fails to start at all, this unit is also stopped) — still no
ordering guarantee by itself. Always pair a dependency directive with the
matching ordering directive unless you specifically want them racing.

`BindsTo=` is `Requires=` plus **live tracking**: if the bound-to unit stops
or fails *after* both are running, this unit is stopped too — useful for a
unit that's meaningless without its counterpart (a VPN tunnel's
dependent service, a device-backed mount unit). `PartOf=` similarly
propagates stop/restart (not start) — `systemctl restart
redis.service` with a dependent `PartOf=redis.service` unit also restarts
that dependent.

## 2. Templated / instantiated units — one file, many instances
```ini
# /etc/systemd/system/worker@.service
[Unit]
Description=Worker instance %i

[Service]
ExecStart=/opt/app/worker --queue %i
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
```bash
systemctl enable --now worker@high-priority.service
systemctl enable --now worker@low-priority.service
systemctl status worker@high-priority
```
`%i` is the instance name (everything after `@`), substituted verbatim —
use `%I` instead if the instance name needs unescaping (contains `-` encoded
as a path, common when the instance comes from a device/mount path).
`worker@.service` itself (no instance) is the template and is never started
directly.

## 3. Socket activation — start on first connection, not at boot
```ini
# myapp.socket
[Socket]
ListenStream=8080
Accept=no

[Install]
WantedBy=sockets.target
```
```ini
# myapp.service (same base name — systemd pairs them automatically)
[Service]
ExecStart=/opt/app/myapp
# the service inherits the already-bound listening socket via fd 3 (sd_listen_fds)
```
```bash
systemctl enable --now myapp.socket    # NOT myapp.service — socket owns the port, starts the service on first connection
ss -tlnp | grep 8080                    # port is bound even before myapp.service has ever run
```
The port is bound immediately, but the service process only starts on the first connection. With `Accept=no` the service receives the listening socket itself; with `Accept=yes` a service instance is spawned per connection and a template `myapp@.service` is required.


## 4. OnFailure — act when a unit fails, without polling
```ini
[Unit]
OnFailure=alert-oncall@%n.service
OnFailureJobMode=replace
```
`%n` expands to the failed unit's own name, so one generic
`alert-oncall@.service` template (see section 2) can handle alerting for
every unit that references it. This fires when the unit enters the failed state; `OnSuccess=` is the counterpart for units that finish successfully.


## 5. Timers — the advanced half, past `OnCalendar=`
```ini
[Timer]
OnCalendar=*-*-* 02:00:00
OnCalendar=*-*-* 14:00:00     # multiple OnCalendar lines are additive, not overwritten
Persistent=true                # catch up a missed run if the box was off
AccuracySec=1min                # how much systemd may slip the exact time to batch wakeups (default 1min)
RandomizedDelaySec=10m          # spread a fleet's identical timers to avoid a thundering herd
```
```bash
systemd-analyze calendar "*-*-* 02:00:00" --iterations=3   # verify the expression before trusting it
systemctl list-timers --all                                 # next + last run for every timer, including inactive ones
```
A timer's companion unit defaults to the same base name
(`backup.timer` → `backup.service`) unless `Unit=` in `[Timer]` overrides
it — a renamed `.service` file with the old `.timer` left pointing at the
default name is a quiet way to have a timer "running" that triggers nothing
useful.

## Gotchas
- `systemctl daemon-reload` is required after editing a template or adding
  `OnFailure=` just like any unit edit — forgetting it is the single most
  common "my change didn't take effect" report (see the service-management
  skill's drop-in notes for the same point).
- `BindsTo=`/`PartOf=` create a *live* coupling — adding one to a unit that
  shares infrastructure with several others can cause an unrelated restart
  to cascade further than intended; audit with `systemctl list-dependencies
  --reverse <unit>` before adding either directive in a shared/critical path.
- A `.socket` unit left enabled with its paired `.service` unit *disabled*
  still accepts connections and starts the service transiently on first
  connect — `systemctl is-enabled myapp.service` showing `disabled` doesn't
  mean the app can't start; check the socket unit's state too.


## Verify
- [ ] Every `Wants=`/`Requires=` has a matching `After=`/`Before=` unless racing is genuinely intended.
- [ ] `systemctl list-dependencies --reverse <unit>` was checked before adding `BindsTo=`/`PartOf=` to a shared unit.
- [ ] `systemd-analyze calendar "<expr>" --iterations=3` matches the intended schedule before enabling a timer.
- [ ] A deliberate failure of a unit with `OnFailure=` actually triggers the configured follow-on unit (`journalctl -u <alert-unit>` confirms).
- [ ] `systemctl list-timers --all` shows the expected next-run time for every active timer, with no orphaned timer pointing at a renamed/missing service.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: `Wants=`/`Requires=`/`BindsTo=`/`PartOf=` semantics and the advice to pair `BindsTo=` with `After=` (`systemd.unit`); `OnFailure=` and `OnFailureJobMode=` (default `replace`); `OnSuccess=`; `%n` and `%i`/`%I`; `Accept=` and the matching service or template (`systemd.socket`); `AccuracySec=` default 1min, `RandomizedDelaySec=`, `Persistent=`, multiple `OnCalendar=` lines and the default companion unit (`systemd.timer`); `systemd-analyze calendar --iterations=`. Removed claims about crash behaviour of socket-activated services and silent OnCalendar parsing.

Method: documentation only; no commands were run.
