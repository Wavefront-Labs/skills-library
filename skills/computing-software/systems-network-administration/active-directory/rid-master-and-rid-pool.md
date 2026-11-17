---
id: computing-software.systems-network-administration.active-directory.rid-master-and-rid-pool
name: rid-master-and-rid-pool
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, rid-master, rid-pool, fsmo, dcdiag, sid]
level: advanced
status: docs-checked
description: "Monitor and protect the RID master: per-DC RID pools, global RID space warnings (events 16656/16657), unlocking the 31st bit, and spotting runaway object creation."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/managing-rid-issuance
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# RID master and RID pools

**Goal:** never be unable to create users, groups or computers.

## Mechanics
- Every security principal's SID = domain SID + RID. RIDs come from a **global space** per domain: by default 2^30
  (1,073,741,823) RIDs, roughly one billion principals. Starting in Windows Server 2012 the 31st bit can be unlocked,
  raising the global pool to 2,147,483,648 RIDs.
- The RID master hands each DC a block of RIDs. The default block is **500**; the registry value `RID Block Size` under
  `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\RID Values` can override it, but since 2012 a value above 15,000 is
  treated as 15,000 and the DC logs event 16653 at every reboot.
- The attribute `rIDAvailablePool` on `CN=RID Manager$,CN=System,DC=<domain>` holds the global RID space.

## Check health
```cmd
Dcdiag.exe /TEST:RidManager /v
```
Microsoft's guide uses `Dcdiag.exe /TEST:RidManager /v | find /i "Available RID Pool for the Domain"` to read the
available pool (2,147,483,647 after an unlock instead of 1,073,741,823).

## Built-in warnings (Windows Server 2012+, Directory-Services-SAM source)
- Event **16658**: periodic warning on every DC as the remaining global RID space shrinks (first one at about 107
  million RIDs remaining in a default domain, then at increasing rates).
- **RID ceiling enforcement**: an artificial ceiling at ten percent of the global space remaining. Within one percent
  of it, DCs requesting pools log warning **16656**. At the ceiling the RID master logs **16657** and issues no further
  pools until you override it; DCs keep using the blocks they already hold. Ceiling trigger points: 966,367,640 in a
  default domain, 1,932,735,282 with an unlocked 31-bit space.
- Event **16655** (informational) is logged when the global maximum has been increased; **16654** when a pool was
  invalidated (expected with virtual DC safeguards).

## If consumption is abnormal
Creating over 100 million objects is not expected; Microsoft says to investigate user, computer and group creation
processes in the domain immediately.

## Remove the ceiling block
With the RID master on a Windows Server 2012+ DC, bind to it in LDP.exe as a domain administrator and replace
`msDS-RIDPoolAllocationEnabled` with `TRUE` on `CN=RID Manager$,CN=System,DC=<domain>` (the attribute returns to NOT SET
on the next allocation). Follow Microsoft's step-by-step procedure.

## Unlock the 31st bit (last resort)
Only when RIDs are really running out, together with ceiling enforcement. The documented method is an LDP modify on the
blank-DN rootDSE that adds `SidCompatibilityVersion` = `1`, then confirming event 16655. It cannot be reverted except by
a full forest recovery. Windows Server 2003/2008 DCs cannot issue RIDs once it is unlocked (2008 R2 only with KB
2642658), no functional level enforces this, and some applications may mishandle SIDs from the unlocked pool.

## Verify
- [ ] Monitoring alerts on events 16656, 16657 and 16658 from Directory-Services-SAM.
- [ ] `Dcdiag.exe /TEST:RidManager /v` passes.
- [ ] Every DC in the domain is Windows Server 2012 or later before any unlock.

## Checked

Documentation: Microsoft Learn "Managing RID Issuance" (updated 2025-05), from MicrosoftDocs/windowsserverdocs and MicrosoftDocs/windows-powershell-docs, main branch (latest commits 2026-10-23).
Confirmed: global space 2^30 and the 31st-bit unlock (SidCompatibilityVersion = 1 via LDP), block size 500 and the
15,000 cap with event 16653, ceiling enforcement at ten percent with events 16656/16657 and the trigger points,
msDS-RIDPoolAllocationEnabled override, events 16654/16655/16658, the Dcdiag command, the old-DC caveats.
Wrong or removed: the claim that a DC requests a new pool at 50 percent use (not in the docs), event 16645 as the
exhaustion event, the "soft ceiling at 90 percent remaining" description (the ceiling is at ten percent remaining),
event 16648, 16656 described as a 10-percent-step warning on the master, the PowerShell rIDAvailablePool arithmetic
and "RIDs are never reused".

Method: documentation only; no commands were run.
