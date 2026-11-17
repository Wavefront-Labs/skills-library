---
id: computing-software.systems-network-administration.linux.tuned-recommend-and-verify
name: tuned-recommend-and-verify
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tuned, tuned-adm-verify, tuned-recommend, tuned-adm, configuration-drift, performance-tuning]
level: practitioner
status: docs-checked
description: "Check that a tuned profile is really applied: tuned-adm recommend/active/verify, reading /var/log/tuned/tuned.log for drift, and fixing settings overridden by other tools."
sources:
  - https://github.com/redhat-performance/tuned/blob/master/man/tuned-adm.8
  - https://github.com/redhat-performance/tuned/blob/master/recommend.conf
  - https://github.com/redhat-performance/tuned
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# tuned-adm recommend and verify

## Recommended vs active
```bash
tuned-adm recommend        # static rules: virt-what output and /etc/system-release-cpe (e.g. virtual-guest in a VM), else balanced
tuned-adm active           # current profile(s)
tuned-adm list             # available profiles with descriptions
tuned-adm profile_info virtual-guest
```
Default rules live in `/usr/lib/tuned/recommend.d/50-tuned.conf`; override with `/etc/tuned/recommend.conf`
(evaluated first) or files in `/etc/tuned/recommend.d/` (same file name wins over the one in `/usr/lib`);
files are evaluated alphabetically and the first matching entry is used.
`tuned-adm auto_profile` switches back to automatic selection; `tuned-adm profile_mode` shows the current mode.
`recommend_command = 0` in `tuned-main.conf` disables the command and hard-codes `balanced`.

## Verify the system matches the profile
```bash
tuned-adm verify                         # 'Verification succeeded' or lists failures
tuned-adm verify --ignore-missing        # skip settings unsupported on this hardware
grep -E 'ERROR|verify' /var/log/tuned/tuned.log | tail -20
```
`tuned-adm verify` prints "Verification succeeded, current system settings match the preset profile." or
"Verification failed, current system settings differ from the preset profile."; the log has the detail of what is
checked, the value set and the value expected, so something else changed any mismatching value.

## Typical drift sources
- `/etc/sysctl.d/*.conf` applied after tuned (or a `sysctl -p` in a script) — decide one owner; put it in a custom tuned profile or remove the conflict.
- Kernel command-line options in the profile (`[bootloader]`) need a reboot to verify.
- Configuration management or other services writing the same sysctl/sysfs values.
- `reapply_sysctl=1` (default) re-applies the system sysctl files after tuned's values; `reapply_sysctl_exclude` lists keys to leave alone.

## Dynamic tuning
`dynamic_tuning` in `/etc/tuned/tuned-main.conf` lets tuned change settings at runtime (every `update_interval`, default 10 s), so verify output can fluctuate; the shipped file sets it to 0.

## Verify
- [ ] `tuned-adm verify` succeeds after reboot; no repeated errors in tuned.log.

## Checked

Checked 2026-10-26 against redhat-performance/tuned master (last commit 2026-09-10): man/tuned-adm.8, recommend.conf, man/tuned-main.conf.5 and the verify messages in tuned/admin. Confirmed: recommend uses virt-what output and /etc/system-release-cpe, recommend.conf then recommend.d evaluation order, auto_profile and profile_mode, verify -i and its result messages, log path, dynamic_tuning and reapply_sysctl behaviour. Corrected: bare metal is not always throughput-performance (rules key on the CPE string), and the invented verify log line was replaced.

Method: documentation only; no commands were run.
