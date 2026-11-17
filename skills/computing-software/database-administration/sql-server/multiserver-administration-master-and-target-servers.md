---
id: computing-software.database-administration.sql-server.multiserver-administration-master-and-target-servers
name: multiserver-administration-master-and-target-servers
category: computing-software
field: database-administration
product: sql-server
tags: [database-administration, sql-server, mssql, multi-server-jobs, msx, tsx, sql-server-agent, master-server, target-server]
level: advanced
status: docs-checked
description: "Run SQL Server Agent jobs centrally with multiserver administration: master (MSX) and target (TSX) servers, enlistment rules, and channel encryption."
sources:
  - https://learn.microsoft.com/en-us/sql/ssms/agent/automated-administration-across-an-enterprise
  - https://learn.microsoft.com/en-us/sql/ssms/agent/create-a-multiserver-environment
  - https://learn.microsoft.com/en-us/sql/ssms/agent/set-encryption-options-on-target-servers
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Multiserver administration (MSX / TSX)

A **master server** (MSX) distributes jobs to, and receives events from, **target servers** (TSX), and stores the central copy of the job definitions. Targets connect periodically to update their job schedule: a new job on the master is downloaded, and after running it the target reconnects and reports status. Define a backup job (steps, operators to notify, schedule) once on the master, enlist each server as a target, and they all run it.

## Rules and considerations
- Needs at least one master and one target. The feature is for sysadmin members; a sysadmin on the target cannot edit the operations the master performs there.
- Not supported on Azure SQL Managed Instance.
- Use the most recent version as the master; the current and two previous versions are supported.
- A target reports to only one master: defect it before enlisting it elsewhere. Defect before renaming a target and re-enlist after. To dismantle the setup, defect every target.
- Integration Services supports only targets at the same or higher version than the master.
- With many targets, avoid a performance-sensitive production server as the master, because target traffic can slow it.
- The Agent service account must be in the `msdb` role `TargetServersRole` on the master; the Master Server Wizard adds it during enlistment.
- Make a master, make a target, enlist and defect are documented as tasks in Learn (SSMS wizards and the procedures it lists).

## Channel encryption
Full TLS encryption and certificate validation are on by default between master and targets. If you cannot use a certificate but still want an encrypted channel, set the target's registry value `MsxEncryptChannelOptions` (REG_DWORD) under `SQLServerAgent` for the instance:

| Value | Meaning |
|---|---|
| 0 | encryption disabled; only if the channel is secured another way |
| 1 | encryption without certificate validation |
| 2 | full TLS and certificate validation (default; keep unless you have a reason) |

With 1 or 2, TLS must be enabled on both servers; with 2, a properly signed certificate must be on the master. Back up the registry before editing it.

## Monitor and troubleshoot
Learn documents these catalog objects and procedures for multiserver work: `systargetservers`, `sysjobservers`, `sp_help_targetserver`, `sp_help_jobserver`, `sp_help_downloadlist` and `sp_resync_targetserver`. Related Learn topics cover polling servers, managing events, and troubleshooting multiserver jobs that use proxies. Job definitions must be the same where they do database work.

## Alternatives
Registered servers in SSMS are a separate way to work with many instances.

## Verify
Every target is enlisted to exactly one master and job status from each target shows on the master.

## Checked
2026-11-09. Read in full: "Automated Administration Across an Enterprise", "Create a multiserver environment" and "Set Encryption Options on Target Servers". Removed (not on those pages): the T-SQL enlist and job-creation examples, MSXOperator and error 14363, polling interval and status codes, error-log troubleshooting hints, and the Ola Hallengren and dbatools comparison.
Method: documentation only; no commands were run.
