---
id: computing-software.systems-network-administration.backup-and-recovery.bacula-virtual-full-and-migration-jobs
name: bacula-virtual-full-and-migration-jobs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [bacula-virtualfull, bacula-migration-job, bacula, bacula-copy-job, next-pool, bareos]
level: advanced
status: docs-checked
description: "Build Bacula virtual full backups from existing backups and move jobs between pools with Migrate jobs and Next Pool; Bareos Always Incremental builds on virtual backups."
sources:
  - https://www.bacula.org/15.0.x-manuals/en/main/Migration_Copy.html
  - https://docs.bareos.org/TasksAndConcepts/AlwaysIncrementalBackupScheme.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bacula VirtualFull and Migrate jobs

**Goal:** fresh full backups without reading the client again, and data moved from one pool and storage to another automatically.

## VirtualFull
Setting the Job level to `VirtualFull` consolidates the previous Full, the most recent Differential and any later Incrementals into a new Full without contacting the client: Bacula reads the previous backup data and writes it to a volume in a different pool. Other products call this synthetic backup or consolidation. The new Full counts as the most recent Full for later Incrementals and Differentials.

The manual's example (jobs write to `Default`, whose `NextPool` is `Full`, which uses an autochanger storage):
```
Pool {
  Name = Default
  Pool Type = Backup
  Volume Retention = 365d
  NextPool = Full
  Storage = File
}
Pool {
  Name = Full
  Pool Type = Backup
  Volume Retention = 365d
  Storage = DiskChanger
}
```
```
run job=MyBackup level=VirtualFull
```
- Bacula reads from the pool in the Job resource and writes to the Next Pool. Writing to a different pool avoids a read/write deadlock on the same volume. You can point Next Pool at the current pool: Bacula does not allow reading and writing the same Volume, so this normally works.
- A later restore that involves the most current Full reads the VirtualFull volumes, whichever pool they are in.
- If no prior Jobs exist, the Virtual Full fails with an error.
- The Start and End time of the Virtual Full are set to those of the last job included, so the next Incremental backs up everything since that job.
- To choose a point in time, give a JobId: `run job=Vbackup jobid=3 level=VirtualFull` selects the previous Full, previous Differential (if any) and later Incrementals up to that job. An explicit list such as `jobid=4-7` merges exactly those jobs; the new level is Differential if the list contains a Differential, otherwise Incremental. Jobs unrelated to the current Job are discarded; use `alljobid=` to merge jobs with different names.

## Migrate
A Migrate job moves data to the pool named by the source pool's `Next Pool` (and its storage). In the manual's example the Default pool has `Next Pool = Tape` and `Storage = File`, and the Tape pool uses the `DLTDrive` storage:
```
Job {
  Name = "migrate-volume"
  Type = Migrate
  Level = Full
  Client = rufus-fd
  FileSet = "Full Set"
  Messages = Standard
  Pool = Default
  Maximum Concurrent Jobs = 4
  Selection Type = Volume
  Selection Pattern = "File"
}
```
Running it migrates all volumes in the Default pool matching the regular expression `File` to the Tape pool. With `Selection Type = Job` and `Selection Pattern = ".*Save"`, all jobs whose name ends in Save are migrated instead. Client, FileSet and Level are present in the example though selection is by pool and pattern.

## Bareos Always Incremental
Bareos (16.2.4 and later) builds on virtual backups: client backups are always Incremental, and incrementals older than a configured age are consolidated into a new backup every day by a job with `Type = Consolidate`.
- Job directives: `Accurate = yes` (required, so deleted files are not kept in the consolidated jobs), `Always Incremental = yes`, `Always Incremental Job Retention`, `Always Incremental Keep Number`.
- At least two storages are needed; the pool's `Next Pool` receives the consolidated jobs.
- Run the incrementals in the backup window and the consolidation during the day.
- It is only suitable for file-based backups (not VMware plugins or NDMP).

## Checked
2026-11-07. Read Migration_Copy as fetched: the text begins mid-page at the Pool/Storage example, so the page's introductory text, the Migration/Copy directive lists and the Copy-job discussion were not in the fetched text and could not be read. Read the first 95 lines of the Bareos Always Incremental page (concept, Job directives, Consolidate job, storages and pools start); the later sections (Max Full Consolidations, Max Full Age, multi-client examples) were not read. Removed because the pages do not confirm them: the list of selection types (SmallestVolume, PoolOccupancy, PoolTime, PoolUncopiedJobs ...), Migration Time and High/Low Bytes pool directives, the Copy job description and `list copies`, "original job records are purged after Migrate", "Accurate = yes needed" for Bacula VirtualFull (confirmed only for Bareos Always Incremental), the two-devices requirement, `status dir`/wait gotchas, the `Next Pool` override claim and the invented Verify step. Configuring_Director was dropped from sources because its fetched text contains none of the Job or Pool directives cited.
Method: documentation only; no commands were run.
