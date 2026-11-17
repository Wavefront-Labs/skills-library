---
id: computing-software.systems-network-administration.active-directory.replication-health-monitoring
name: replication-health-monitoring
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, repadmin, repadmin-replsummary, replication-health, repadmin-showrepl, get-adreplicationfailure, get-adreplicationpartnermetadata, monitoring, scheduled-report]
level: practitioner
status: docs-checked
description: "Watch AD replication daily: repadmin /replsummary and /showrepl CSV, Get-ADReplicationFailure, deltas vs link intervals, and an alerting script."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/diagnose-replication-failures
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adreplicationfailure
  - https://learn.microsoft.com/en-us/powershell/module/activedirectory/get-adreplicationpartnermetadata
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc835092(v=ws.11)
  - https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-server-2012-r2-and-2012/cc742012(v=ws.11)
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Monitor AD replication health

## Daily checks
```cmd
repadmin /replsummary                 :: per-DC largest delta and fail counts
repadmin /showrepl * /csv > showrepl.csv
repadmin /queue *                     :: inbound queue should be near 0
```
Read `/replsummary`: the **largest delta** for each source/destination should be below the
site link replication interval plus margin (intra-site: minutes). Any non-zero `fails` with
an error code is actionable.

## PowerShell equivalent for alerting
```powershell
$dcs = (Get-ADDomainController -Filter *).HostName
$fail = foreach ($dc in $dcs) { Get-ADReplicationFailure -Target $dc -ErrorAction SilentlyContinue }
$stale = foreach ($dc in $dcs) {
  Get-ADReplicationPartnerMetadata -Target $dc -Partition * -ErrorAction SilentlyContinue |
    ? { $_.LastReplicationSuccess -lt (Get-Date).AddHours(-24) } }
if ($fail -or $stale) { $fail,$stale | Out-String | Send-YourAlert }   # replace with your alerting
```
Run as a scheduled task (gMSA) on a management server every hour.

## Also check
- `dcdiag /test:replications /e /q` weekly.
- Directory Service log events 1311 (KCC topology problem), 1865, 2042 (tombstone lifetime
  exceeded), 1988 (lingering object), 2087/2088 (DNS lookup failures for partners).
- DFSR SYSVOL backlog (separate from AD replication).

## Force replication when testing
```cmd
repadmin /syncall /AdeP          :: all partitions, push, enterprise, by DN
repadmin /replicate DC02 DC01 "DC=ad,DC=example,DC=com"
```

## Gotchas
- A DC approaching the tombstone lifetime without replicating (default 180 days on supported versions, 60 on older
  forests) is an emergency: it must not replicate again without checks (see the replication error 8614 article).

## Verify
- [ ] Alert fires in a test (block 135 between two DCs in a lab for an interval).
- [ ] Baseline: zero fails, deltas within interval, across all DCs.

## Checked
2026-10-27, against the repadmin /replsummary, /showrepl and /queue pages (Learn previous-versions, Windows Server 2012 R2), the Get-ADReplicationFailure and Get-ADReplicationPartnerMetadata cmdlet pages, and the replication troubleshooting articles. Confirmed: /replsummary and its /bysrc, /bydest, /errorsonly, /sort:delta options; `/showrepl * /csv`; /queue takes a DSA list; Get-ADReplicationFailure returns the failures currently associated with the target (so no extra filter is needed); Get-ADReplicationPartnerMetadata -Target -Partition and the LastReplicationSuccess property; events 1311, 1865, 2042, 1988, 2087/2088; tombstone lifetime defaults. Removed as unconfirmed: the FailureCount filter, other output property names, the ">60 days" display claim and the RODC remark.

Method: documentation only; no commands were run.
