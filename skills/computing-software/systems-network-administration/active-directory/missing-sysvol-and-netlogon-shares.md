---
id: computing-software.systems-network-administration.active-directory.missing-sysvol-and-netlogon-shares
name: missing-sysvol-and-netlogon-shares
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, sysvol-netlogon-shares, sysvol-replication, dfsr]
level: advanced
status: docs-checked
description: "Fix a DC that is not sharing SYSVOL and NETLOGON: SysvolReady, DFSR initial sync waits (4614), dirty shutdown (2213), content freshness (4012) and safe repair order."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-missing-sysvol-and-netlogon-shares
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/force-authoritative-non-authoritative-synchronization
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/dfsr-event-id-2213
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Missing SYSVOL and NETLOGON shares

A DC without these shares fails Group Policy and logon scripts for clients that pick it, and the dcdiag `NetLogons` test
fails.

## Check
```cmd
net share
dcdiag /test:netlogons /test:sysvolcheck /test:advertising /s:<DC>
```
`SysVolCheck` reads the Netlogon `SysvolReady` registry value (it must exist with value 1; FRS or DFSR); `NetLogons`
checks that SYSVOL and NETLOGON can be read and that the needed network-access rights exist.

## Causes and fixes
1. **New DC, initial sync not complete**: DFS Replication log event **4614** (waiting for initial replication) without
   **4604** (SYSVOL initialised). The upstream partner is usually in an error state; fix it, then run
   `dfsrdiag pollad` on the new DC to trigger the initial sync.
2. **Dirty shutdown pause** (event **2213**): run the `ResumeReplication` WMI method of `DfsrVolumeConfig` using the
   exact command in the event text (it logs 2214 when recovery completes). Prefer this to deleting the DFSR database,
   which makes the server's data nonauthoritative.
3. **Content freshness** (event **4012**): replication stopped because it had failed for longer than
   `MaxOfflineTimeInDays` (60 when content freshness is enabled, 0 when disabled). Follow the Microsoft procedure for a
   nonauthoritative synchronization (set `msDFSR-Enabled` to FALSE on the DC's DFSR member object, replicate, set it to
   TRUE, and wait for 4614 then 4604). Use an authoritative sync on one DC only when every DC has logged 4012.
4. **Still on FRS**: migrate SYSVOL to DFSR (FRS is a removed feature; see `dfsrmig` reference).

## Do not
Reinitialize DFSR or copy policies by hand while a DC is simply waiting on initial sync: the Microsoft guidance says the
reinitialization is unnecessary in most cases and can cause data loss, and it hides the root cause.

## Verify
- [ ] Event 4604 present, both shares listed, `dcdiag /test:netlogons` passes, `gpupdate` on a client using that DC works.

## Checked

Date: 2026-10-27. Documentation: Microsoft Support "Troubleshoot missing SYSVOL and NETLOGON shares" and "force an
authoritative and non-authoritative synchronization for DFSR-replicated SYSVOL", DFSR event 2213 article, dcdiag
reference, Features removed or no longer developed in Windows Server (MicrosoftDocs repositories, main branch).
Confirmed: events 4614, 4604, 4012, 2213, 2214, `MaxOfflineTimeInDays` values, `ResumeReplication` method,
`msDFSR-Enabled` toggle, `dfsrdiag pollad`, dcdiag `SysVolCheck`/`NetLogons`/`Advertising` descriptions.
Removed unconfirmed claims: the junction-path repair with `mklink`, the Netlogon registry command, setting SysvolReady by
hand, and the "partner backlog" check detail.

Method: documentation only; no commands were run.
