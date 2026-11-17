---
id: computing-software.systems-network-administration.active-directory.dc-backup-strategy-and-tombstone-lifetime
name: dc-backup-strategy-and-tombstone-lifetime
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-recovery, dc-backup-strategy, tombstone-lifetime, repadmin-showbackup]
level: practitioner
status: gated
description: "Design AD backups: which DCs, how often, retention bound by tombstone lifetime, offline and immutable copies, and monitoring with event 2089."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-backing-up-a-full-server
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/ntds-replication-event-2089-backup-latency-interval
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/virtual-dc/restore-virtualized-domain-controller
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# DC backup strategy and tombstone lifetime

## What to back up
- At least **two DCs per domain**, with the system state of each forest, domain and application partition covered
  every day (Microsoft's recommendation in the event 2089 article); include a DC holding FSMO roles and a GC, ideally
  in different sites.
- Full server (bare-metal) backup or system state. System state includes the AD data and log files, the registry, the
  system volume and parts of the OS. The forest recovery guide's backup procedure selects "Full server (recommended)".

## Frequency and retention
- Daily. AD changes constantly; an old backup means more re-work after recovery.
- Useful shelf life is bounded by the **tombstone lifetime** (TSL). Check it:
```powershell
(Get-ADObject "CN=Directory Service,CN=Windows NT,CN=Services,$((Get-ADRootDSE).configurationNamingContext)" -Properties tombstoneLifetime).tombstoneLifetime
```
  Microsoft Support documents the default as 180 days for a forest created on Windows Server 2003 SP1 or later and
  60 days in other cases. Microsoft's restore guidance is to restore a system state backup within the tombstone
  lifetime.
- Keep at least one copy **offline or immutable** (air-gapped disk, immutable cloud vault), and protect the backup
  server as Tier 0. A backup stored on AD-joined systems that domain admins can reach is not safe from an attacker with
  those rights.

## Monitor
Event **2089** (Directory Service log, NTDS Replication) is logged once a day for each writable partition that has not
been backed up within the backup latency interval. The default interval is half the TSL; override it with the
`Backup Latency Threshold (days)` DWORD value under `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters`.
Microsoft suggests setting it so the event appears if no backup is made for about two days.
`repadmin /showbackup *` shows the last backup time per partition
(gated: unconfirmed, source is paywalled or blocked). The readable repadmin reference does not list `/showbackup`, so check `repadmin /?` on a DC.

## Test
Restore a DC backup into an isolated network on a schedule, and rehearse a forest recovery with the recovery guide.

## Verify
- [ ] Every partition backed up within the last 24 hours (event 2089 absent); offline copy date recorded; last restore
  test date.

## Checked

Date: 2026-10-27. Documentation: Microsoft Support "NTDS Replication Event 2089" (2026-02), AD Forest Recovery Guide
backup page, Restore a virtual domain controller, repadmin reference (Windows Server 2012 R2 archive page) (MicrosoftDocs repositories, main branch).
Confirmed: event 2089 behaviour and registry value name, half-TSL default, TSL defaults of 180 and 60 days, the TSL
attribute location, system state contents, restore within TSL, two-DCs-per-partition recommendation.
Gated: `repadmin /showbackup`.
Removed unconfirmed claims: "empty tombstoneLifetime means 60", ransomware targeting claims, the quarterly test and
annual exercise cadence, and the 24-hour verify threshold as a Microsoft number (it is this skill's own target).

Method: documentation only; no commands were run.
