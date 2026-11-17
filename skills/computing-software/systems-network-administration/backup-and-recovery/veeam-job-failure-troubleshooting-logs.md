---
id: computing-software.systems-network-administration.backup-and-recovery.veeam-job-failure-troubleshooting-logs
name: veeam-job-failure-troubleshooting-logs
category: computing-software
field: systems-network-administration
product: backup-and-recovery
tags: [veeam-logs, veeam-backup-job, veeam, troubleshooting, vss-writers, transport-mode]
level: advanced
status: draft
description: "Troubleshoot failed Veeam backup jobs: read the session, find logs on server, proxy and guest, common VSS, snapshot, transport and repository errors, support export."
sources:
  - https://www.veeam.com/kb1832
  - https://helpcenter.veeam.com/docs/backup/vsphere/overview.html?ver=120
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Veeam job failure troubleshooting

## 1. Read the session first
Job → Statistics: per-VM status and the **first** error line. Note the step (snapshot
creation, guest processing, data transfer, finalising), proxy and repository used, and
transport mode ([nbd], [hotadd], [san]).

## 2. Logs (default `%ProgramData%\Veeam\Backup\`)
| Where | Log |
|---|---|
| Backup server | `<JobName>\Job.<JobName>.log`, per-VM `Task.<VM>.log` |
| Backup server | `Svc.VeeamBackup.log` (service), `Svc.VeeamMount.log` (restores) |
| Proxy (Windows) | `%ProgramData%\Veeam\Backup\<JobName>\Agent.*.log` |
| Proxy/repo (Linux) | `/var/log/VeeamBackup/<JobName>/Agent.*.log` |
| Guest (app-aware) | `%ProgramData%\Veeam\Backup\VeeamGuestHelper_*.log` inside the VM (or the guest interaction proxy) |
Export for support: Help → Support Information (select jobs and time range); KB1832
describes collection.

## 3. Common failures
| Error (abridged) | Likely cause | Fix |
|---|---|---|
| "Failed to create VM snapshot" / "An error occurred while taking a snapshot" | vCenter/host issue, VSS quiesce timeout, datastore space, existing stuck snapshots | check vCenter tasks, consolidate, free space; disable VMware Tools quiescence if Veeam app-aware is used |
| "VSSControl: Failed to freeze guest" / "VSS writer failed" | guest VSS writer error | `vssadmin list writers` in guest, restart writer service, check shadow storage |
| "Cannot connect to host" / "NFC storage connection is unavailable" | port 902 to ESXi blocked (NBD), DNS | open 902, fix DNS resolution of host names from proxy |
| HotAdd fails, falls back to NBD | proxy VM on different host/datastore access, disk already hot-added elsewhere | fix proxy placement, remove leftover hot-added disks from proxy VM |
| "Not enough storage space on repository" | retention/space | extend, adjust retention, check SOBR extents and immutability blocking deletes |
| "Changed block tracking cannot be enabled" / CBT errors | VM has snapshots or CBT corrupted | reset CBT |
| "Unable to truncate SQL logs" | permissions of guest account on SQL | grant sysadmin or required rights to the guest processing account |

## 4. Retry and confirm
Retry the job (only failed VMs process), check the new session. Recurring failures at the
same step: open a case with logs.

## Gotchas
- Warnings ("Failed to index guest file system", "Changed block tracking disabled") matter:
  they degrade restores or speed; don't ignore them for weeks.
- Antivirus on proxies/repositories scanning backup files causes slowdowns and
  locking: exclude Veeam paths and processes per Veeam KB.

## Verify
Job succeeds on retry and on the next scheduled run; root cause documented in the ticket.
