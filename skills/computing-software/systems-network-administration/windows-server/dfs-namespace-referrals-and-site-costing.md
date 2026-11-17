---
id: computing-software.systems-network-administration.windows-server.dfs-namespace-referrals-and-site-costing
name: dfs-namespace-referrals-and-site-costing
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, dfs-namespaces, dfs-referrals, site-costing, target-priority, referral-ordering, insite-referrals, dfsutil, referral-cache-ttl, client-failback]
level: practitioner
status: docs-checked
description: "Control which DFS target clients use: lowest-cost/random/exclude-outside-site ordering, target priority overrides, client failback, referral TTLs and dfsutil diagnostics."
sources:
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/set-the-ordering-method-for-targets-in-referrals
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/set-target-priority-to-override-referral-ordering
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/enable-or-disable-referrals-and-client-failback
  - https://learn.microsoft.com/en-us/windows-server/storage/dfs-namespaces/change-the-amount-of-time-that-clients-cache-referrals
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/set-dfsnfoldertarget
  - https://learn.microsoft.com/en-us/powershell/module/dfsn/set-dfsnfolder
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DFS referrals and site costing

A referral is the ordered list of targets a client receives. Order depends on AD sites.

## Ordering methods (namespace or folder level)
- **Lowest cost**: targets in the client's site first (random order among them),
  then other sites from lowest to highest cost, random within equal cost.
- **Random order**: same-site first (random), then the remaining targets in random order.
- **Exclude targets outside of the client's site**: no cross-site fallback; if no same-site target exists the client gets no referral (targets with priority First/Last among all targets are still listed).
In PowerShell, `-EnableSiteCosting` selects lowest cost, `-EnableInsiteReferrals` selects exclude-outside-site, and omitting both selects random order.
```powershell
Set-DfsnRoot -Path '\\ad.example.com\files' -EnableSiteCosting $true
Set-DfsnFolder -Path '\\ad.example.com\files\Software' -EnableInsiteReferrals $true   # exclude targets outside the client's site
```

## Target priority (override)
Force a primary target regardless of site, e.g. a hub server for read-write data while a
replica exists only for DR. `-ReferralPriorityClass` accepts GlobalHigh, SiteCostHigh, SiteCostNormal, SiteCostLow and GlobalLow:
```powershell
Set-DfsnFolderTarget -Path '\\ad.example.com\files\Finance' -TargetPath '\\fs01\Finance$' -ReferralPriorityClass GlobalHigh
Set-DfsnFolderTarget -Path '\\ad.example.com\files\Finance' -TargetPath '\\fs02\Finance$' -ReferralPriorityClass GlobalLow
```
For read-write data replicated by DFSR, give clients a **single active target** to avoid conflicting edits.

## Client failback
If a target becomes unavailable, clients fail over to another target. With **client failback** enabled (`Set-DfsnRoot` or `Set-DfsnFolder -EnableTargetFailback $true`) they return to the preferred target once it is restored; the clients must meet the failback requirements in the DFS Namespaces client documentation. Folders inherit the setting from the namespace root.

## Cache TTLs
Root referral 300 seconds and folder referral 1800 seconds by default (`-TimeToLiveSec`). Lower before
planned target changes.

## Diagnose from a client
```cmd
dfsutil cache /?                  :: display or flush the client referral cache
dfsutil diag /?                   :: diagnostics, including viewing DFS paths
```
Targets in the client's AD site are always listed first, so make sure every client subnet is mapped to a site.

## Verify
- [ ] Clients in each site resolve to their local target.
- [ ] Failback works after a target returns online.

## Checked

Checked 2026-10-25 against the MicrosoftDocs/windowsserverdocs and windows-powershell-docs (Windows Server 2025 DFSN/DFSR modules) repositories, latest commit 2026-10-23. Confirmed: same-site-first referral rule and the three ordering methods; the cmdlet-to-method mapping (`-EnableSiteCosting`, `-EnableInsiteReferrals`, neither means random); exceptions for First/Last-among-all-targets priority; `-ReferralPriorityClass` values; `-EnableTargetFailback` semantics and folder inheritance; default referral TTLs of 300 and 1800 seconds. Removed the claim that lowest cost is the default ordering and the specific `dfsutil cache referral` and `viewdfspath` subcommands, which the checked pages do not state.

Method: documentation only; no commands were run.
