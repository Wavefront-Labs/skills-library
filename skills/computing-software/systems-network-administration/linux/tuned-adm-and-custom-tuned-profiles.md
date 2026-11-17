---
id: computing-software.systems-network-administration.linux.tuned-adm-and-custom-tuned-profiles
name: tuned-adm-and-custom-tuned-profiles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tuned, tuned-adm, custom-tuned-profile, tuned-conf, performance-profiles, throughput-performance, virtual-guest, rhcsa, sysadmin]
level: practitioner
status: docs-checked
description: "Apply and verify tuned profiles with tuned-adm (recommend, profile, verify), and write a custom profile that inherits a stock one and adds sysctl, vm, disk and script settings."
sources:
  - https://github.com/redhat-performance/tuned/blob/master/man/tuned-adm.8
  - https://github.com/redhat-performance/tuned/blob/master/man/tuned.conf.5
  - https://github.com/redhat-performance/tuned/blob/master/man/tuned-main.conf.5
  - https://github.com/redhat-performance/tuned/blob/master/tuned/consts.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tuned-adm and custom tuned profiles

**Goal:** one command applies a coherent set of kernel/CPU/disk tunings for the machine's
role, survives reboots, and drifts are detectable.

## 1. tuned-adm
```bash
dnf install tuned && systemctl enable --now tuned
tuned-adm list                     # available profiles, current one
tuned-adm active
tuned-adm recommend                # what tuned suggests for this hardware/virt
tuned-adm profile virtual-guest    # apply (RHCSA task)
tuned-adm profile throughput-performance my-overrides   # stack several (later wins)
tuned-adm verify                   # checks settings still match; details in /var/log/tuned/tuned.log
tuned-adm off                      # stop tuning (settings revert)
```
Common stock profiles: `balanced`, `powersave`, `throughput-performance` (servers),
`latency-performance`, `network-latency`, `network-throughput`, `virtual-guest`,
`virtual-host`, `hpc-compute`, plus vendor ones (`sap-hana`, `mssql`, `oracle` in tuned-profiles-* packages).

## 2. Custom profile
```bash
mkdir -p /etc/tuned/profiles/myapp
```
```ini
# /etc/tuned/profiles/myapp/tuned.conf
[main]
summary=myapp DB host: throughput-performance + DB tweaks
include=throughput-performance

[sysctl]
vm.swappiness=10
vm.dirty_background_ratio=3
net.core.somaxconn=4096

[vm]
transparent_hugepages=never

[disk]
devices=sdb,sdc
readahead=>4096

[cpu]
force_latency=cstate.id:1

[script]
script=${i:PROFILE_DIR}/script.sh
```
`script.sh` receives `start`/`stop`; use for settings without a plugin, and make `stop` undo them.
```bash
tuned-adm profile myapp && tuned-adm verify
```
Profiles under `/etc/tuned/profiles/` take precedence over same-named ones under
`/usr/lib/tuned/profiles/` (current upstream layout; the installed version's `tuned.conf(5)` names the
directories it reads). Copy-and-edit a stock profile under the same name only if you accept missing
future fixes; `include=` is better.

## Gotchas
- With `reapply_sysctl=0` in `tuned-main.conf`, tuned's `[sysctl]` values override the system sysctl
  files; with `reapply_sysctl=1` (the documented default) tuned re-applies `/run/sysctl.d`,
  `/etc/sysctl.d` and `/etc/sysctl.conf` after its own values, so those win. Know which one owns a key;
  `reapply_sysctl_exclude` protects keys that other services set at run time.
- Dynamic tuning (`dynamic_tuning` in `tuned-main.conf`) changes settings over time (every
  `update_interval`, default 10 s); disable it when benchmarking. The shipped file sets it to 0.
- Profile changes for `[bootloader]` (kernel args) need a reboot.
- `tuned-ppd` (a separate daemon in the tuned project) can stand in for power-profiles-daemon on
  desktops; it maps power profile requests (for example `balanced-battery`) to tuned profiles.

## Verify
- [ ] `tuned-adm active` shows the profile after reboot.
- [ ] `tuned-adm verify` reports "Verification succeeded".
- [ ] `sysctl vm.swappiness` and `cat /sys/kernel/mm/transparent_hugepage/enabled` show your values.

## Checked

Checked 2026-10-26 against the redhat-performance/tuned repository (master, last commit 2026-09-10): man/tuned-adm.8, man/tuned.conf.5, man/tuned-main.conf.5, tuned/consts.py, profiles/ and the cpu plugin documentation. Confirmed: tuned-adm subcommands (list, active, profile with later profile winning, verify with -i/--ignore-missing, recommend, off), profile directories (USER_PROFILES_DIR /etc/tuned/profiles, system /usr/lib/tuned/profiles, user wins), stock profile names, include= and [script] syntax, reapply_sysctl default (True) and semantics, dynamic_tuning shipped as 0 with update_interval 10 s, force_latency syntax (cstate.id:N). Removed: the unconfirmed Fedora version claim and the undocumented cstate.id_no_zero form.

Method: documentation only; no commands were run.
