---
id: computing-software.systems-network-administration.active-directory.sysvol-dfsr-health-and-authoritative-restore
name: sysvol-dfsr-health-and-authoritative-restore
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, sysvol-replication, dfsr-authoritative-sysvol, dfsr]
level: advanced
status: docs-checked
description: "Check SYSVOL DFSR health, find stopped or journal-wrapped DCs, and perform authoritative or non-authoritative SYSVOL sync via msDFSR-Options."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/force-authoritative-non-authoritative-synchronization
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-missing-sysvol-and-netlogon-shares
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/dfsr-event-id-2213
  - https://learn.microsoft.com/en-us/powershell/module/dfsr/get-dfsrbacklog
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# SYSVOL DFSR health and authoritative restore

AD replication can be perfect while SYSVOL is not: GPOs then apply inconsistently depending on which DC a client hits.

## Health checks
```powershell
Get-WmiObject -Namespace root\microsoftdfs -Class dfsrreplicatedfolderinfo -ComputerName <DC> |
  Select ReplicatedFolderName,State   # 0 Uninitialized, 1 Initialized, 2 Initial Sync, 3 Auto Recovery, 4 Normal, 5 In Error
Get-DfsrBacklog -GroupName 'Domain System Volume' -FolderName 'SYSVOL Share' -SourceComputerName <DC1> -DestinationComputerName <DC2>
```
Events in the DFS Replication log:
- **2213** replication paused after dirty shutdown: resume with the `ResumeReplication` WMI method shown in the event; **2214** is logged when dirty-shutdown recovery completes.
- **4012** stopped replicating longer than MaxOfflineTimeInDays (60 by default; 0 means content freshness is off): recover that DC non-authoritatively. Use authoritative sync only when every DC logged 4012 and shows state 5.
- **4614** then **4604** = initial sync completed; **4602** = SYSVOL initialised as primary member.

## Non-authoritative sync (fix one bad DC)
On the bad DC's object: `CN=SYSVOL Subscription,CN=Domain System Volume,CN=DFSR-LocalSettings,CN=<DC>,OU=Domain Controllers,...`
1. Set `msDFSR-Enabled = FALSE`; force AD replication (for example `repadmin /syncall <DC> /AdeP`).
2. On the DC: `dfsrdiag pollad`; wait for event **4114**.
3. Set `msDFSR-Enabled = TRUE`; replicate; `dfsrdiag pollad`; event **4614** then **4604** = synced from partners.

## Authoritative sync (all DCs bad; rebuild from one good copy)
1. Set the DFS Replication service to Manual and stop it on all DCs.
2. On the good DC's subscription object (the PDC emulator is preferred) set `msDFSR-Enabled = FALSE` and `msDFSR-options = 1`.
3. On all other DCs set `msDFSR-Enabled = FALSE`. Replicate AD.
4. Start DFSR on the good DC; event 4114; set its `msDFSR-Enabled = TRUE`; replicate; `dfsrdiag pollad`; event
   **4602** (SYSVOL initialised).
5. Start DFSR on the other DCs (each logs 4114), set their `msDFSR-Enabled = TRUE`, replicate, run `dfsrdiag pollad` on
   each, then return the DFS Replication service to Automatic on all DCs.

## Gotchas
- Never copy files into SYSVOL on several DCs manually; data that does not match partners can end up in the PreExisting and Conflict and Deleted folders.
- Back up SYSVOL contents on each DC before any sync; PreExisting and Conflict and Deleted are purged if initial sync is repeated.
- If you make one DC authoritative, every other DC must be synced non-authoritatively, or you get conflicts.

## Verify
- [ ] All DCs State 4, zero backlog, identical GPO folder counts under Policies.

## Checked
2026-10-27, against the Microsoft Learn articles "How to force authoritative and non-authoritative synchronization for DFSR-replicated sysvol" (updated 2026-02), "Troubleshoot missing SYSVOL and NETLOGON shares" and "DFSR event ID 2213", plus the Get-DfsrBacklog cmdlet page. Confirmed: msDFSR-Enabled and msDFSR-options=1 sequences and events 4114, 4602, 4614, 4604; DFSR state values 0 to 5; MaxOfflineTimeInDays default 60 and event 4012; event 2213 and ResumeReplication, event 2214; `dfsrdiag pollad`; PDC emulator preferred as authoritative; SYSVOL backup advice. Removed as unconfirmed: dfsrdiag backlog syntax (replaced with Get-DfsrBacklog), events 2104/2004/5002/5008, the %SystemRoot%\SYSVOL path, the ConflictAndDeleted wording. Corrected: the authoritative sequence does not itself state 4614/4604 for the other DCs.

Method: documentation only; no commands were run.
