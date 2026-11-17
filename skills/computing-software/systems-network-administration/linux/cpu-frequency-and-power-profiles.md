---
id: computing-software.systems-network-administration.linux.cpu-frequency-and-power-profiles
name: cpu-frequency-and-power-profiles
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, cpupower, cpufreq, scaling-governor, intel-pstate, amd-pstate, energy-performance-preference, c-states, power-profiles-daemon, tuned-ppd, powerprofilesctl, sysadmin]
level: practitioner
status: docs-checked
description: "Control CPU frequency and power: cpufreq drivers and governors with cpupower, intel_pstate/amd-pstate EPP, C-states, and desktop profiles via power-profiles-daemon or tuned-ppd."
sources:
  - https://docs.kernel.org/admin-guide/pm/cpufreq.html
  - https://docs.kernel.org/admin-guide/pm/intel_pstate.html
  - https://man.archlinux.org/man/cpupower.1
  - https://gitlab.freedesktop.org/upower/power-profiles-daemon
  - https://docs.kernel.org/admin-guide/pm/intel_pstate.html
  - https://docs.kernel.org/admin-guide/pm/amd-pstate.html
  - https://github.com/torvalds/linux/blob/master/tools/power/cpupower/man/cpupower-frequency-set.1
  - https://github.com/torvalds/linux/blob/master/tools/power/x86/turbostat/turbostat.8
  - https://github.com/redhat-performance/tuned
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# CPU frequency, governors and power profiles

**Goal:** pick performance vs power deliberately — max clocks for latency-sensitive servers,
efficient scaling for laptops — and confirm the hardware is actually doing it.

## 1. Inspect
```bash
cpupower frequency-info               # driver, governor, hw limits, current freq, boost
cpupower idle-info                    # C-states and their latency
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver     # the active scaling driver (intel_pstate, an amd-pstate variant, ...)
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_governor
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_preference 2>/dev/null
cat /sys/devices/system/cpu/cpu0/cpufreq/energy_performance_available_preferences 2>/dev/null
grep MHz /proc/cpuinfo | sort | uniq -c       # or: turbostat --quiet --show Busy%,Bzy_MHz,PkgWatt 5
```

## 2. Set governor / EPP
```bash
cpupower frequency-set -g performance          # all CPUs; governors offered are listed in scaling_available_governors
cpupower frequency-set -u 3.0GHz               # cap max frequency (thermal/power budget)
echo <value> | tee /sys/devices/system/cpu/cpu*/cpufreq/energy_performance_preference   # a value from energy_performance_available_preferences
cpupower idle-set -D 10                        # disable idle states whose latency exceeds the given value (latency tuning)
```
With **intel_pstate in active mode**, only the `powersave` and `performance` governors are available, and the
energy-performance preference (EPP) hint (`energy_performance_preference`; amd-pstate also accepts integers 0-255, lower = more
performance) is the main knob. Persist settings with a tuned profile or your distribution's mechanism.

## 3. Desktop/laptop profiles
Desktop environments normally switch profiles through a power-profile service (power-profiles-daemon, or the `ppd` component of the tuned project). Use the tool your distribution ships and run only one power manager at a time, so two tools do not rewrite the same settings.

## Gotchas
- `performance` on laptops costs battery and heat.
- Firmware power settings can limit what the OS can do; check them if the OS settings have no effect.
- With intel_pstate active, only `performance` and `powersave` exist, so a script setting `ondemand` will fail.
- Frequency shown in `/proc/cpuinfo` is a snapshot; use turbostat for measured values.

## Verify
- [ ] `cpupower frequency-info` shows the chosen governor/EPP on every CPU after reboot.
- [ ] Under load, `turbostat` shows expected Bzy_MHz; idle power drops in power-saver.

## Checked

Checked against the Linux kernel documentation tree (torvalds/linux master, latest commit 2026-10-25) (admin-guide/pm intel_pstate, amd-pstate, cpufreq), the kernel-tree `cpupower` man pages and `turbostat(8)`, and the tuned source tree (a `tuned/ppd` component exists) on 2026-10-26. Confirmed: intel_pstate active-mode governors `powersave` and `performance`, `energy_performance_preference` and `energy_performance_available_preferences`, amd-pstate integer EPP 0-255 with lower values favouring performance, cpupower `frequency-set -g/-u` and `idle-set -D`, turbostat `--show` with Busy%, Bzy_MHz, PkgWatt. Removed: power-profiles-daemon command details and Fedora-version claim (its docs could not be read), cpupower service file paths, EPP name list, VM and BIOS claims.

Method: documentation only; no commands were run.
