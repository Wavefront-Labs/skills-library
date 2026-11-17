---
id: computing-software.systems-network-administration.linux.mdadm-raid-scrub-and-check
name: mdadm-raid-scrub-and-check
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, mdadm, software-raid, raid-check, mdadm-scrub, mismatch-cnt, sync-action, raid-repair, lpic-2, sysadmin]
level: practitioner
status: docs-checked
description: "Scrub md RAID arrays to find latent bad sectors before a rebuild does: sync_action check/repair, distro schedules (raid-check, checkarray), mismatch_cnt and throttling."
sources:
  - https://github.com/md-raid-utilities/mdadm/blob/main/md.4
  - https://github.com/md-raid-utilities/mdadm/blob/main/mdadm.8.in
  - https://github.com/md-raid-utilities/mdadm/blob/main/systemd/mdcheck_start.timer
  - https://github.com/md-raid-utilities/mdadm/blob/main/misc/mdcheck
  - https://src.fedoraproject.org/rpms/mdadm/blob/rawhide/f/raid-check
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Scrubbing md RAID

**Goal:** read every sector of every member periodically, so unreadable sectors are found and
rewritten from redundancy now — not discovered during a rebuild when there's no redundancy left.

## 1. Manual
```bash
echo check  > /sys/block/md0/md/sync_action     # read all, compare, count mismatches, rewrite unreadable sectors
echo repair > /sys/block/md0/md/sync_action     # also fix mismatches (RAID5/6: new parity; RAID1/10: copies overwritten from one)
echo idle   > /sys/block/md0/md/sync_action     # stop
cat /proc/mdstat                                 # check = 41.2% …
cat /sys/block/md0/md/mismatch_cnt               # sectors that didn't match after the run
mdadm --action=check /dev/md0                    # equivalent (idle, frozen, check, repair)
```

## 2. Scheduled
- Fedora/RHEL packaging: `/usr/sbin/raid-check` run by `raid-check.timer`, configured in
  `/etc/sysconfig/raid-check` (variables `ENABLED`, `CHECK` = check or repair, `NICE`, `SKIP_DEVS`).
- Upstream mdadm: `mdcheck` script with `mdcheck_start.timer` (`OnCalendar=Sun *-*-1..7 0:45:00`, the first Sunday of each month)
  and `mdcheck_continue.timer`; `mdcheck --continue` only continues previously started checks, `--start` also starts new ones.
- Debian and Ubuntu package their own scheduled check; see their mdadm package documentation.

## 3. Reading results
- A read error during a scrub is handled by the normal read-error path: correct data comes from the other devices and is written back. Several on one disk → check its SMART, plan replacement.
- `mismatch_cnt` is reset when a scrub starts and counts sectors in the IO units found inconsistent (128 may mean one 64 KB unit). Non-zero:
  - RAID1/10 with a swap partition or swap file on the array: mismatches are expected, because swap may change a page while it is being written to both copies.
  - A check right after `mdadm --create --assume-clean` is also expected to find mismatches.
  - Otherwise run `repair`, then `check` again; investigate if it reappears.
  `repair` on RAID1/10 overwrites all but one copy with that one, so md cannot know which copy was correct.

## 4. Impact
Throttled by `/proc/sys/dev/raid/speed_limit_min` (the goal speed while other activity is present) and `speed_limit_max` (when idle), both in KiB/s per device. Lower min if production latency suffers, or run during low-traffic windows; `mdcheck` can run time-boxed slices across nights (its `--duration` option).

## Gotchas
- A check that is interrupted before finishing leaves the end of the disks unchecked; the upstream `mdcheck --continue` timer resumes it, custom scripts often don't.
- Scrubbing doesn't replace SMART long tests and vice versa; do both.
- Hardware RAID has its own "patrol read"/"consistency check" — md tools don't see it.

## Verify
- [ ] The scheduled check is enabled (`systemctl list-timers` shows `raid-check` or `mdcheck_start`).
- [ ] `mismatch_cnt` is 0 for parity arrays after the latest check.

## Checked

Checked against the mdadm main branch (md.4 SCRUBBING AND MISMATCHES, mdadm.8.in `--action`, systemd/mdcheck_start.timer, misc/mdcheck) and the Fedora mdadm package (src.fedoraproject.org, raid-check and mdadm.spec, rawhide), repository last pushed 2026-10-08.
Confirmed: `check`, `repair`, `idle` in sync_action; `mismatch_cnt` semantics and the swap-on-RAID1 explanation; what `repair` writes; `mdadm --action=`; the upstream mdcheck timers and schedule; raid-check variables; speed limit units.
Removed unconfirmed claims: the mdadm 4.2 version gate, the Debian checkarray and cron specifics (the Debian packaging files could not be fetched), kernel log message texts, and the monthly/weekly frequency advice.

Method: documentation only; no commands were run.
