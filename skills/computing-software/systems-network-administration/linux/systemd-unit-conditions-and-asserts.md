---
id: computing-software.systems-network-administration.linux.systemd-unit-conditions-and-asserts
name: systemd-unit-conditions-and-asserts
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, systemd, unit-file, unit-conditions, conditionpathexists, conditionvirtualization, assertpathexists, conditionfirstboot, conditionhost, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Make units start only where they should with Condition*= and Assert*=: path, host, virtualisation, kernel command line, first boot, and how skipped vs failed shows up."
sources:
  - https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Conditions%20and%20Asserts
  - https://www.freedesktop.org/software/systemd/man/latest/systemd-detect-virt.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Unit conditions and asserts

**Goal:** one unit file that is safe to ship everywhere but only runs where its
preconditions hold — and that tells you clearly why it didn't.

## 1. Condition vs Assert
- `Condition…=` false → unit is **skipped**: not started, not failed, dependencies proceed.
  The failed check is logged.
- `Assert…=` false → the start job **fails** and is logged loudly; the unit itself does not enter the failed state. Use when absence is a real fault.
- Checked at start time (after ordering deps), not at enable time.
- Several conditions are ANDed; prefix with `|` to make a trigger group (ORed among
  themselves, ANDed with the rest). Prefix `!` negates.

## 2. The ones used most
```ini
[Unit]
ConditionPathExists=/etc/app/config.yaml        # file or dir exists
ConditionPathExists=!/etc/app/disabled          # does NOT exist (kill switch)
ConditionPathIsMountPoint=/data
ConditionDirectoryNotEmpty=/var/spool/app
ConditionFileNotEmpty=/etc/app/token
ConditionVirtualization=!container              # also vm, kvm, oracle, docker, wsl, …
ConditionHost=db01                              # hostname or machine-id
ConditionKernelCommandLine=app.debug            # flag or key=value present
ConditionFirstBoot=yes                          # /etc/ was unpopulated at boot (see machine-id(5))
ConditionACPower=true
ConditionEnvironment=APP_MODE=prod              # manager environment (≥ 246)
ConditionMemory=>=4G                            # (v242 and later)
ConditionUser=!root                             # useful in user units
ConditionNeedsUpdate=/etc                       # run once after /usr updated (systemd-update-done)
```
Asserts have the same names with `Assert` prefix (`AssertPathExists=` …).

## 3. Example: optional mount-dependent job
```ini
[Unit]
Description=Nightly export
ConditionPathIsMountPoint=/mnt/backup
After=mnt-backup.mount
[Service]
Type=oneshot
ExecStart=/usr/local/bin/export.sh
```
If the backup disk is absent the timer still fires, the service is skipped, nothing alerts as
failed. Use `AssertPathIsMountPoint=` instead if a missing disk should page someone.

## 4. Debugging
```bash
systemctl status app.service                      # the failed condition is logged
systemd-analyze condition 'ConditionVirtualization=vm' 'ConditionPathExists=/etc/app'   # test without a unit
systemd-detect-virt
```

## Gotchas
- A failed Condition does not fail the start job (it is also not propagated to units that `Require=` this one), so check the unit state rather than assuming it ran.
- Conditions don't re-evaluate later; use a `.path` unit to start when a file appears.


## Verify
- [ ] `systemd-analyze verify` passes and `systemd-analyze condition` returns the expected result.
- [ ] On a host where the condition is false, `systemctl --failed` does not list the unit.
- [ ] `systemctl --failed` stays empty on hosts where the unit should not run.

## Checked

2026-10-25, against the systemd v262.1 documentation (man pages and NEWS in the systemd/systemd repository, main branch). Confirmed: Condition versus Assert semantics (a failed assertion fails the start job without putting the unit in the failed state; failed conditions are not failures and are not propagated to `Requires=`), triggering `|` and negating `!` prefixes, checks happen when the job executes; every Condition/Assert name used exists, including the `ConditionVirtualization=` values (`vm`, `container`, `kvm`, `oracle`, `docker`, `wsl`), `ConditionFirstBoot=` semantics, `ConditionNeedsUpdate=` and `ConditionMemory=` (v242 NEWS, not v244), `ConditionEnvironment=` (v246), `ExecCondition=`; `systemd-analyze condition` and `systemd-detect-virt`. Removed the quoted status text, the ConditionResult properties and the relative-path claim.

Method: documentation only; no commands were run.
