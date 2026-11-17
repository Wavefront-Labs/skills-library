---
id: computing-software.systems-network-administration.linux.tuned-profile-plugins
name: tuned-profile-plugins
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, tuned, tuned-plugins, tuned-conf, sysctl-plugin, disk-plugin, scheduler-plugin, custom-tuned-profile]
level: advanced
status: docs-checked
description: "Write tuned profile sections with the right plugins: [main] include, [sysctl], [vm], [disk] readahead/elevator, [cpu], [scheduler] isolation, [bootloader], [script] and variables."
sources:
  - https://github.com/redhat-performance/tuned/tree/master/tuned/plugins
  - https://github.com/redhat-performance/tuned/blob/master/man/tuned.conf.5
  - https://github.com/redhat-performance/tuned/blob/master/tuned/hardware/device_matcher.py
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# tuned plugins in custom profiles

`/etc/tuned/profiles/db-host/tuned.conf`
```ini
[main]
summary=Database host on top of throughput-performance
include=throughput-performance

[variables]
isolated=8-15

[sysctl]
vm.swappiness=1
vm.dirty_background_ratio=3

[vm]
transparent_hugepages=never

[disk]
devices=nvme*
elevator=none
readahead=>4096            # '>' = only increase, never lower

[cpu]
governor=performance
energy_perf_bias=performance
force_latency=cstate.id:1|10          # max C-state id 1, else 10 us (fallbacks split by '|')

[scheduler]
isolated_cores=${isolated}

[bootloader]
cmdline_db=transparent_hugepage=never

[script]
script=${i:PROFILE_DIR}/script.sh

[service]
service.irqbalance=stop,disable
```
Apply: `tuned-adm profile db-host`; check `tuned-adm verify`.

## Plugin notes
- `[sysctl]` values here override the same keys from included profiles; with `reapply_sysctl=1`
  (default in `tuned-main.conf`) the system sysctl files are re-applied afterwards and win — pick one owner.
- `[disk]`/`[net]` match devices via `devices=` (comma or space separated shell-style globs; a leading `!` excludes);
  `[net]` options include `wake_on_lan`, `coalesce`, `features`, `ring` and `channels`.
- `[bootloader]` options are named `cmdline_<suffix>=args` (`+args` appends, `-args` removes); tuned records the
  result in `/etc/tuned/bootcmdline`, and a reboot is needed.
- `[script]` runs the script with `start`, `stop` and `verify` actions — implement `stop` to undo `start`.
- Instance names: the section name, with `type=` naming the plugin when it differs (`[nvme_disks] type=disk`).
- `${f:...}` built-in functions exist, for example `${f:cpulist2hex:...}` and `${f:exec:...}`.
- `[service]` entries are `service.<name>=<commands>` with commands from `start`, `stop`, `enable`, `disable`
  and an optional `file:<overlay>`.

## Gotchas
- `include=` merges plugin sections by default; `replace=1` in a section makes it replace all options the
  included profile set for the same plugin type and devices.

## Verify
- [ ] `tuned-adm verify` succeeds; spot-check `sysctl vm.swappiness`, `cat /sys/block/nvme0n1/queue/scheduler`.

## Checked

Checked 2026-10-26 against redhat-performance/tuned master (last commit 2026-09-10): plugin sources and their embedded option documentation (plugin_disk, plugin_cpu, plugin_scheduler, plugin_bootloader, plugin_service, plugin_vm, plugin_net, plugin_script), man/tuned.conf.5, device_matcher.py and the throughput-performance profile. Confirmed: device globs with ! exclusion, readahead=>4096, elevator, cmdline_<suffix> with +/- prefixes, /etc/tuned/bootcmdline, isolated_cores, service.<name>=commands, transparent_hugepages, [script] start/stop/verify, replace=1 semantics, ${f:cpulist2hex} and ${f:exec} functions. Removed: kernel.sched_migration_cost_ns, the $tuned_params GRUB variable, the id_no_zero C-state form and the unconfirmed claim that option typos are silently ignored.

Method: documentation only; no commands were run.
