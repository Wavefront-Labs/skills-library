---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-spooling-and-concurrency
name: bacula-spooling-and-concurrency
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula-spooling, maximum-concurrent-jobs, bacula, tape-performance, data-spooling, bareos]
level: advanced
status: docs-checked
description: "Tune Bacula concurrency and data spooling: Maximum Concurrent Jobs at every level, spool directory sizing, attribute spooling, and keeping tape drives streaming."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Data_Spooling.html
  - https://www.bacula.org/15.0.x-manuals/en/problems/Tips_Suggestions.html
  - https://www.bacula.org/15.0.x-manuals/en/main/Configuring_Director.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula spooling and concurrency

**Goal:** many jobs running at once while tape drives write at full speed without shoe-shining.

## Maximum Concurrent Jobs: set it everywhere
Bacula can run jobs concurrently, but the default configuration does not enable it. Set `Maximum Concurrent Jobs` in bacula-dir.conf in the Director, Job, Client and Storage resources (the Director default is 1). The File daemon and the Storage daemon each have their own `Maximum Concurrent Jobs` (default 20 for both). A Device resource in bacula-sd.conf also takes the directive, to cap jobs on one device.
Two jobs backing up the same client to the same storage run together only if the Director, Client and Storage resources in bacula-dir.conf all allow more than 1.

## Data spooling
```
Job { ... Spool Data = yes }
Device {
  ...
  Spool Directory = /srv/bacula-spool
  Maximum Spool Size = 800G           # all jobs on this device
  Maximum Job Spool Size = 200G       # per job
}
```
Without spooling, a slow incremental written straight to tape makes the drive start and stop (shoe-shine), which wears the tape. With spooling the data goes to disk first and is despooled to tape in one fast pass.
- Turning on data spooling automatically turns on attribute spooling, so catalog entries are only inserted if the data really reached the volume. Attributes are despooled to the Director near the end of the job, and the tape drive may be idle during that insert.
- Always set a maximum spool size. A full data-spool disk is detected and the job despools and continues, but if the disk holding spooled attributes fills, the job is cancelled.
- Exclude the spool directory from backups, or the spool file is backed up into itself and the job ends in error.
- Do not put the spool directory on the same partition as the Bacula working directory; jobs can fail in odd ways when it fills.

## Other tuning
- `Maximum Network Buffer Size` and `Maximum block size` are Storage daemon directives. The default block size is 64,512 bytes. Setting `Maximum block size` on a modern LTO drive can reduce shoe-shine and raise performance; check the Storage daemon chapter before changing it.

## Verify
Job reports show despooling at the drive's speed, and `status storage` shows several jobs running at once.

## Checked
2026-10-28. Confirmed against the Bacula 15.0.x manual pages Data Spooling, Tips and Suggestions (concurrent jobs section, defaults of 1 and 20) and Storage Daemon Configuration (spool directives, block size default). Removed because the pages do not show them: the Job and Device default claims, the quoted "waiting on max jobs" message, `Spool Attributes = yes`, `Prefer Mounted Volumes`, the LTO-9 speed figure, the 1M block size advice and interleaving claims.
Method: documentation only; no commands were run.
