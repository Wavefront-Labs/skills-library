---
id: computing-software.systems-network-administration.active-directory.ad-ldap-performance-diagnostics
name: ad-ldap-performance-diagnostics
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, dcdiag, ldap-performance, expensive-ldap-queries, field-engineering-logging, ntds-performance-counters, event-1644]
level: advanced
status: docs-checked
description: "Diagnose domain controller load and slow LDAP: NTDS counters, event 1644 expensive and inefficient query logging, Server Performance Advisor/AD diagnostics, and fixes."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/event1644reader-analyze-ldap-query-performance
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/active-directory-server/ldap-considerations
  - https://learn.microsoft.com/en-us/windows-server/administration/performance-tuning/role/active-directory-server/memory-usage-considerations
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD performance and LDAP query diagnostics

## Is the DC overloaded?
Counters (Performance Monitor or `Get-Counter`):
```powershell
Get-Counter '\NTDS\Request Latency','\NTDS\Estimated Queue Delay' -SampleInterval 5 -MaxSamples 12
```
- Request latency depends on how long requests take to process; AD times out requests after 120 seconds by default,
  so look for changes against your own baseline rather than an absolute threshold.
- Estimated queue delay should be near 0; a sustained higher value means requests are waiting for ATQ LDAP threads.
- The ESE database cache can grow to the size of NTDS.dit and a larger cache improves DC performance, so a DC that
  is short of RAM serves more queries from disk.

## Find expensive queries (event 1644)
Requires enhanced 1644 logging (built into Windows Server 2012 R2 and later). On each DC:
```powershell
$d='HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Diagnostics'
Set-ItemProperty $d 'Field Engineering' 5
$p='HKLM:\SYSTEM\CurrentControlSet\Services\NTDS\Parameters'
New-ItemProperty $p 'Expensive Search Results Threshold' -Value 10000 -PropertyType DWord -Force
New-ItemProperty $p 'Inefficient Search Results Threshold' -Value 1000 -PropertyType DWord -Force
New-ItemProperty $p 'Search Time Threshold (msecs)' -Value 100 -PropertyType DWord -Force
```
The two results thresholds shown are the defaults (10,000 and 1,000). The default search-time threshold is 30,000 ms;
100 ms is a starting value to lower as you tune. No restart is needed. Field Engineering logging at 5 adds other
events to the Directory Service log, so reset it to its default of 0 when you stop collecting.
Analyse saved Directory Service logs from many DCs with Microsoft's Event1644Reader.ps1 (it builds Excel pivot
tables).

## Typical fixes
- A filter on an unindexed attribute: add an index through the schema, or change the query. Note that a paged
  query can use only one index.
- Narrow the search base instead of searching from the domain root for a known OU.
- Apps polling every few seconds: cache the result or use change notifications.
- Many NTLM authentications: Netlogon's `MaxConcurrentApi` may need tuning (see the capacity-planning guide).

## Data Collector Set
Performance Monitor > Data Collector Sets includes the Active Directory Diagnostics set on domain controllers; it is
one of the documented ways to detect inefficient queries.

## Verify
- [ ] Top expensive queries identified with client IPs and owners; estimated queue delay back near 0.

## Checked
2026-10-27. Documentation: Microsoft Learn Event1644Reader article, AD Server performance tuning (LDAP and memory
considerations) and capacity planning. Confirmed: the Field Engineering value 5 and the three registry values with
defaults (30,000 ms, 10,000 and 1,000), no restart needed, reset to 0 afterwards, enhanced 1644 logging from Windows Server
2012 R2; `NTDS\Request Latency` and `NTDS\Estimated Queue Delay` counters and the 120-second request timeout;
single-index limit for paged queries; Active Directory Diagnostics Data Collector Set; ESE cache can grow to the NTDS.dit
size. Removed as unconfirmed: the other NTDS counter names, the lsass CPU rule of thumb, the `searchFlags` bit detail,
the leading-wildcard and negation scan claims and the DirSync suggestion.
Method: documentation only; no commands were run.
