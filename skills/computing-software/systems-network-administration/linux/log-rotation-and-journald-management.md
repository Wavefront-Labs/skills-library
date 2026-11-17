---
id: computing-software.systems-network-administration.linux.log-rotation-and-journald-management
name: log-rotation-and-journald-management
category: computing-software
field: systems-network-administration
product: linux
tags: [linux, logrotate, journald, journalctl, systemd-journal, log-rotation, vacuum, systemmaxuse, rsyslog, disk-full, retention, copytruncate, sysadmin, journald-persistent, logrotate-d]
level: practitioner
status: docs-checked
description: "Keep logs from filling the disk or vanishing on reboot: logrotate configuration, journald persistence/size caps, and the copytruncate trap."
sources:
  - https://github.com/logrotate/logrotate/blob/main/logrotate.8.in
  - https://www.freedesktop.org/software/systemd/man/latest/journald.conf.html
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Log rotation and journald management — logs that don't fill the disk or vanish

**Goal:** make sure logs survive a reboot when they need to, get capped
before they fill `/var`, and rotate without losing in-flight writes — the
two systems (logrotate for plain files, journald for the binary journal)
need different handling and are often both present on the same box.

## 1. journald — persistence is opt-in
```bash
journalctl --disk-usage                      # how much the journal is currently using
mkdir -p /var/log/journal                    # with Storage=auto, the directory's existence selects persistent storage
systemctl restart systemd-journald
```
With `Storage=auto` the journal is **volatile** (`/run/log/journal`,
tmpfs, gone on reboot) unless `/var/log/journal` exists — creating that
directory is the entire switch, no config edit required, but it's easy to
assume persistence is already on until the first reboot after an incident
loses exactly the logs needed for the postmortem.

```ini
# /etc/systemd/journald.conf
[Journal]
Storage=persistent
SystemMaxUse=1G          # cap total disk used by the journal
SystemMaxFileSize=100M    # per-file rotation size within that cap
MaxRetentionSec=2week     # age-based eviction regardless of size
```
```bash
journalctl --vacuum-size=500M       # retroactively shrink to a size now, doesn't change future growth
journalctl --vacuum-time=2weeks      # retroactively drop anything older
```
Without a `SystemMaxUse=` cap, the journal grows until it hits a built-in
default of 10% of the filesystem it lives on (capped at 4G) — on a box with `/var` on
the root filesystem, an uncapped journal is a real path to filling the root
disk and taking the whole system down, not just losing old logs.

## 2. logrotate — plain-text application logs
```
# /etc/logrotate.d/myapp
/var/log/myapp/*.log {
    daily
    rotate 14
    compress
    delaycompress
    missingok
    notifempty
    create 0640 myapp myapp
    sharedscript
    postrotate
        systemctl kill -s HUP myapp.service > /dev/null 2>&1 || true
    endscript
}
```
`logrotate` itself runs via a cron job or systemd timer (`logrotate.timer`
on modern distros) that processes all of `/etc/logrotate.d/*` — it's not a
daemon watching files continuously, so changes to a config only take effect
at its next scheduled run (or `logrotate -f <config>` to force one for
testing).

## 3. The `copytruncate` trap
```
/var/log/myapp/app.log {
    daily
    copytruncate      # copies the file then truncates the original IN PLACE
}
```
Default logrotate behavior **renames** the log file and creates a new one
with the original name — a well-behaved app that opened the file once
keeps writing to the renamed (now rotated) file's inode until it's told to
reopen (the `postrotate` HUP signal above is exactly that instruction).
`copytruncate` exists for apps that **can't** be told to reopen their log
file (no signal handler, closed-source, or you don't control it) — it
copies the current content elsewhere then truncates the live file to zero
in place, so the app keeps its same file descriptor valid. The cost: a
**race window** between the copy and the truncate where anything the app
writes in that gap is lost — acceptable for low-volume logs, a real risk
for anything high-throughput. Prefer the rename+signal pattern whenever the
application supports it; reach for `copytruncate` only when it genuinely
can't.

## 4. Diagnosing "disk full, logs did it"
```bash
du -sh /var/log/* | sort -rh | head -10        # biggest log consumers
journalctl --disk-usage                         # journal's own current size
find /var/log -name '*.log' -size +500M          # any single file that grew past rotation without being caught
lsof +L1                                          # files deleted but still held open by a process (classic hidden disk-usage-without-a-visible-file cause)
```
`lsof +L1` catches the case where `du`/`df` disagree because a process
still holds an open file descriptor to a deleted (rotated-and-removed, or
just `rm`'d) file — the space isn't freed until every holding process
closes or exits, even though no path on disk references it anymore.
`systemctl restart <service>` (reopening its fds) or killing the process is
the actual fix, not another round of deleting files that look gone already.

## 5. rsyslog/syslog interaction
On boxes still running `rsyslog` (forwarding/filtering syslog-protocol
messages, common even alongside journald for shipping to a central log
server), journald's `ForwardToSyslog=` controls forwarding to a syslog daemon; by default only
forwarding to wall is enabled, and the man page notes forwarding has no effect if nothing
reads the socket. Check how your distribution connects rsyslog to journald, since a
mismatch gives duplicate or missing lines on the forwarding side.

## Gotchas
- Rotating a log a running process still has open **without** signaling it
  to reopen leaves it writing to a now-unlinked (deleted) inode — disk
  space isn't reclaimed (same `lsof +L1` symptom above) even though the
  rotation "succeeded" and the old file is gone from `ls`.
- journald's `SystemMaxUse=` is a *ceiling*, not a target — setting it too
  close to genuinely needed retention means a busy period evicts logs
  faster than expected right when they're most wanted for debugging that
  busy period.
- `logrotate`'s `rotate N` count combined with `compress`/`delaycompress`
  interacts with disk usage non-linearly — `delaycompress` keeps the most
  recent rotated file uncompressed (so a `tail`/grep on it doesn't need
  decompression), meaning actual peak disk usage is higher than `rotate N
  * average-compressed-size` naive math suggests.
- A container's `stdout`/`stderr` logs (captured by the container runtime's log driver) bypass both logrotate and journald
  entirely unless the runtime's own log driver is configured with rotation
  — a containerized app can fill disk via its runtime's log driver while
  `journalctl`/`logrotate` both look perfectly healthy.

## Verify
- [ ] `journalctl --disk-usage` stays under the configured `SystemMaxUse=`, and `/var/log/journal` exists if persistence across reboot is required.
- [ ] `logrotate -d /etc/logrotate.d/<config>` (dry run) shows the expected rotation schedule and file count with no syntax errors.
- [ ] A rotated application's log continues growing in the NEW file post-rotation (confirms the reopen/HUP signal actually worked), not still writing into the old renamed file.
- [ ] `lsof +L1` is checked whenever `du` and `df` disagree about free space — no deleted-but-open file descriptors silently holding space.
- [ ] Container log drivers (if applicable) have their own rotation configured — not assumed covered by host-level logrotate/journald.

## Checked

Checked 2026-10-27 against systemd journald.conf(5) and journalctl(1) man page sources, logrotate(8) man page source (logrotate/logrotate master) and lsof(8) source (lsof-org/lsof master), 2026-10-27. Confirmed: Storage=auto behaviour and /var/log/journal, SystemMaxUse default of 10% capped at 4G, SystemMaxFileSize and MaxRetentionSec names, ForwardToSyslog default, journalctl --disk-usage/--vacuum-size/--vacuum-time, logrotate cron or logrotate.timer scheduling, copytruncate behaviour and its small data-loss window, lsof +L1 selecting unlinked open files. Removed or softened: the tmpfiles command, the claim that many distributions default to volatile, the rsyslog socket description, the Docker json-file driver name.

Method: documentation only; no commands were run.
