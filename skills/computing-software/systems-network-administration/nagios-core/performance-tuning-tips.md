---
id: computing-software.systems-network-administration.nagios-core.performance-tuning-tips
name: performance-tuning-tips
category: computing-software
field: systems-network-administration
product: nagios-core
tags: [systems-network-administration, nagios-core, tuning, performance, max-concurrent-checks, check-latency, check-result-reaper-frequency, aggressive-host-checking, ramdisk, enable-environment-macros]
level: advanced
status: docs-checked
description: "Tune Nagios Core: max_concurrent_checks sizing from -s, reaper settings, passive over active, compiled plugins, cheap host checks, no aggressive host checking, fast disks."
sources:
  - https://assets.nagios.com/downloads/nagioscore/docs/nagioscore/4/en/tuning.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Tuning tips

1. Graph performance with MRTG (`computing-software.systems-network-administration.nagios-core.nagiostats-mrtg`).
2. `use_large_installation_tweaks` on.
3. `enable_environment_macros` off if scripts get macros as arguments.
4. `check_result_reaper_frequency` and `max_check_result_reaper_time`: in Core 4+ they affect only passive results.
5. `max_concurrent_checks`: start at the minimum reported by `nagios -s`, double, and raise until average service latency is low. Latency over about 10-15 s means check starvation.
6. Prefer passive checks where an external app can do the monitoring.
7. Avoid interpreted plugins; use compiled ones (or `perlcc` for Perl).
8. Cheap host checks: `max_check_attempts` ~10 with one ICMP packet via `check_ping`, not attempts 1 with 10 packets; or `check_fping`.
9. Schedule regular host checks (`check_interval` > 0).
10. Enable cached host checks (`computing-software.systems-network-administration.nagios-core.cached-checks`).
11. Leave `use_aggressive_host_checking` off unless recoveries are missed.
12. Hardware: disk is the bottleneck; avoid slow/NFS storage, use SSD; a RAM disk can hold `objects.cache` and `status.dat`.

Fast restart: `computing-software.systems-network-administration.nagios-core.fast-startup-precache`. Large sites: `computing-software.systems-network-administration.nagios-core.large-installation-tweaks`.

## Checked

2026-11-04. Confirmed each of the twelve tips on the Tuning page: MRTG graphing, use_large_installation_tweaks, enable_environment_macros, reaper settings affecting only passive results in Core 4, max_concurrent_checks sizing from nagios -s and the 10 to 15 second latency warning, passive checks, compiled plugins with perlcc, one-packet host checks, scheduled host checks, cached host checks, use_aggressive_host_checking, and disks (SSD, RAM disk for objects.cache and status.dat). Nothing removed.

Method: documentation only; no commands were run.
