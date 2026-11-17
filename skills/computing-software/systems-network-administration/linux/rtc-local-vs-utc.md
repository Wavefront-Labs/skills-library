---
id: computing-software.systems-network-administration.linux.rtc-local-vs-utc
name: rtc-local-vs-utc
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, rtc-local, utc-vs-local, hwclock, rtc, timedatectl, set-local-rtc, adjtime, dual-boot, windows-realtimeisuniversal, clock, sysadmin]
level: intro
status: gated
description: "Decide and fix whether the hardware clock (RTC) holds UTC or local time: timedatectl set-local-rtc, hwclock, /etc/adjtime, Windows dual-boot and boot-time clock jumps."
sources:
  - https://github.com/systemd/systemd/blob/main/man/timedatectl.xml
  - https://github.com/util-linux/util-linux/blob/master/sys-utils/hwclock.8.adoc
  - https://github.com/mlichvar/chrony/blob/master/doc/chrony.conf.adoc
  - https://github.com/libvirt/libvirt/blob/master/docs/formatdomain.rst
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RTC in UTC vs local time

**Goal:** the battery-backed hardware clock and the OS agree, so the clock is right at boot
(before NTP), logs don't jump by hours, and dual-boot machines stop fighting.

## 1. The rule
Keep the RTC in **UTC** on every Linux-only machine and every server. Local-time RTC exists
for Windows compatibility and breaks twice a year (DST) because the RTC doesn't know about DST.

## 2. Inspect
```bash
timedatectl                       # "RTC in local TZ: no" is what you want
hwclock --show --verbose          # RTC reading and how it's interpreted
cat /etc/adjtime                  # third line: UTC or LOCAL
```
Symptom of a mismatch: after reboot the system clock is off by the UTC offset until NTP corrects it.

## 3. Fix
```bash
timedatectl set-local-rtc 0                  # keep the RTC in UTC; also syncs the RTC from the system clock
timedatectl set-local-rtc 0 --adjust-system-clock   # instead sync the system clock from the RTC, using the new setting
hwclock --systohc --utc                      # write the (correct, NTP-synced) system time to the RTC as UTC
```
With chrony's `rtcsync` directive (in the sample configuration) the kernel copies system time to the RTC every 11 minutes on Linux.

## 4. Dual-boot with Windows
Better: make Windows use UTC instead of switching Linux to local time. In Windows (admin):
`reg add "HKLM\System\CurrentControlSet\Control\TimeZoneInformation" /v RealTimeIsUniversal /d 1 /t REG_DWORD /f`
then reboot (gated: unconfirmed, source is paywalled or blocked). No readable Microsoft documentation for this value was found. If you must keep Windows on local time: `timedatectl set-local-rtc 1` in Linux and
accept the problems with time zone and DST changes that timedatectl warns about.

## Gotchas
- VMs: libvirt guests default to a UTC hardware clock; Windows guests expect `<clock offset='localtime'/>`.
- Local-time RTC is "not fully supported" per timedatectl(1); avoid it on servers.
- `hwclock` uses the drift data in `/etc/adjtime` when reading the RTC; `--update-drift` with `--systohc` recalculates it.

## Verify
- [ ] `timedatectl` reports `RTC in local TZ: no` and `RTC time` equals `Universal time` (within a second).
- [ ] After a reboot with network disabled, `date -u` is correct before NTP syncs.

## Checked

2026-10-26. systemd timedatectl(1): set-local-rtc behaviour, --adjust-system-clock, the warning about local-time RTC, third line of /etc/adjtime. util-linux master (last commit 2026-10-26) hwclock(8): --systohc, drift handling from adjtime. chrony.conf: rtcsync and the 11 minute kernel copy on Linux. libvirt formatdomain: UTC default and localtime for Windows. The Windows RealTimeIsUniversal registry value could not be confirmed and carries the gated marker. Removed unchecked claims about Kerberos, fsck and deleting adjtime.

Method: documentation only; no commands were run.
