---
id: computing-software.systems-network-administration.active-directory.directory-service-event-ids
name: directory-service-event-ids
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, directory-service-events, event-1311, event-2042, event-1388]
level: advanced
status: docs-checked
description: "Read the Directory Service event log on DCs: what events 1311, 1865, 1388, 1988, 2042, 2087, 2088, 1925 and 13508 mean and what to do for each."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8614
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/active-directory-replication-event-id-2042
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/information-lingering-objects
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/troubleshoot-event-id-1311-messages
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8524
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/enable-ldap-signing-in-windows-server
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/event1644reader-analyze-ldap-query-performance
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/networking/troubleshoot-missing-sysvol-and-netlogon-shares
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Directory Service event IDs that matter

```powershell
Get-WinEvent -ComputerName DC01 -FilterHashtable @{LogName='Directory Service'; Level=1,2,3; StartTime=(Get-Date).AddDays(-1)} |
  Group Id | Sort Count -Desc | ft Count,Name
```

| ID | Meaning | Action |
|---|---|---|
| 1311 | KCC cannot build a spanning tree; sites are not fully connected | check site links, bridgehead DCs offline, site link bridges |
| 1865 | KCC: sites not connected (follows 1311) | fix site link topology |
| 1925 | Replication link could not be established | DNS, RPC, firewall to partner; `repadmin /showrepl` |
| 2087 / 2088 | DNS lookup of partner failed (2087); 2088 = partner resolved by NetBIOS name, which only happens after DNS fails | fix the `<DSA GUID>._msdcs.<forest root>` CNAME records and DNS client settings |
| 2042 | It has been too long since this server last replicated with the named source | check for lingering objects first; then demote/rebuild or follow the 8614 procedure |
| 1988 / 1388 | Lingering object detected (1988 is logged on the destination that blocks it and means the source holds the lingering object; 1388 means the destination received an update for an object it should have had) | `repadmin /removelingeringobjects` or Lingering Object Liquidator |
| 2095 | USN rollback detected | demote and rebuild the DC |
| 1645 | No authenticated RPC to a DC: its SPN is not registered on the KDC DC that resolved it | check the partner's SPNs and time sync |
| 2889 | Clients doing unsigned/simple LDAP binds | enable the diagnostic logging to find them, then require signing |
| 1644 | Expensive LDAP query (logged when the Field Engineering diagnostic level is 5) | tune the query or index; Event1644Reader.ps1 helps analysis |
DFS Replication log: 4012 = SYSVOL stopped replicating past MaxOfflineTimeInDays (default 60); 2213 = dirty shutdown, replication paused.

## Workflow
1. Group by ID across all DCs, newest first.
2. For replication events, confirm with `repadmin /replsummary` and `repadmin /showrepl <dc>`.
3. Raise diagnostic logging only when needed:
   `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Diagnostics` (for example `Field Engineering` = 5 for event 1644), then reset it to 0.

## Verify
- [ ] No 1311/2042/1988/2095 across DCs; 2889 count trending to zero.

## Checked
2026-10-27, against Microsoft Learn (SupportArticles-docs current pages). Confirmed: 1311 and 1865 (topology), 1925/2087/2088 (DNS lookup; 2088 resolves by NetBIOS), 1388/1988 (lingering objects), 2042, 2095 (USN rollback), 1645 (SPN not registered on the KDC), 2889 (LDAP signing article), 1644 (Field Engineering level 5, Event1644Reader), DFSR 4012 (MaxOfflineTimeInDays 60) and 2213. Removed as unconfirmed: event 13508 and the "5 Replication Events" diagnostics setting.

Method: documentation only; no commands were run.
