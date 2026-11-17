---
id: computing-software.systems-network-administration.active-directory.dcdiag-test-interpretation
name: dcdiag-test-interpretation
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, dc-health, dcdiag, dcdiag-tests, domain-controller-health, repadmin, ad-health-check]
level: practitioner
status: docs-checked
description: "Run dcdiag and interpret its tests: which failures matter, verbose and DNS tests, known false positives, and the follow-up command for each failing test."
sources:
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/dcdiag
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Interpret dcdiag test results

## Run
```powershell
dcdiag /s:DC01 /v /c /e /q          # all DCs (/e), comprehensive (/c), errors only (/q)
dcdiag /test:dns /e /v             # DNS tests, all DCs in the forest (defaults to /DnsAll)
dcdiag /e /c /v /f:'<vol>:\Logs\dcdiag.txt'
```
Run from a DC or an RSAT machine. Blocking ICMP between hosts prevents DCDiag from working as intended.

## Tests and follow-up
| Test | Failing means | Next step |
|---|---|---|
| Connectivity | DSA or DNS registration not reachable over LDAP/RPC (cannot be skipped) | `nslookup <guid>._msdcs.<forest>`, firewall |
| Advertising | DC not advertising as DC/GC/KDC/time | Netlogon service, `nltest /dsgetdc`, SYSVOL not shared |
| Replications / KccEvent | replication error, replication disabled, latency over 12 hours (Replications); KCC errors in the last 15 minutes (KccEvent) | `repadmin /showrepl`, `repadmin /replsummary` |
| NetLogons / SysVolCheck / FrsEvent / DFSREvent | cannot read SYSVOL/NETLOGON or the network-logon right is missing (NetLogons); SysVolReady not 1 (SysVolCheck); FRS or DFSR event-log errors in the last 24 hours | DFSR health, `Get-SmbShare SYSVOL` |
| MachineAccount | DC computer account missing, outside the Domain Controllers OU, wrong UserAccountControl flags or ServerReference, or missing SPNs | the `/FixMachineAccount` repair option adds the missing UAC flags; avoid `/RecreateMachineAccount` |
| RidManager | RID master not accessible or invalid RID pool values | FSMO holder health |
| Services | an AD-dependent service is not running or has the wrong start type (NTDS, KDC, Netlogon, W32Time, DFSR, Dnscache, SamSs, RpcSs and others) | start/fix service |
| SystemLog | errors or warnings in the System log in the past 60 minutes | read the events |
| VerifyReferences / CrossRefValidation | broken DC reference attributes (VerifyReferences) or invalid partition cross-references (CrossRefValidation) | check the object it names; metadata cleanup if the DC is gone |
| KnowsOfRoleHolders | DC does not know the five FSMO role holders (add `/e` to compare DCs) | `netdom query fsmo` |
| DNS (DnsBasic, DnsForwarders, DnsDelegation, DnsDynamicUpdate, DnsRecordRegistration; not run by default) | DC DNS config/records broken | see DC SRV records skill |

## Known noise
- SystemLog fails on any recent error or warning in the past 60 minutes, harmless or not.
- DFSREvent fails on any DFSR warning or error in the past 24 hours, including from problems already resolved.
- DNS tests without `/e` run only against the target DC; with `/e` they run on every DC and can be slow when DCs are offline.
- Errors immediately after a reboot (services starting): rerun once the DC has settled.

## Routine
Schedule weekly `dcdiag /e /q` plus `repadmin /replsummary` and mail non-empty output.

## Verify
- [ ] `dcdiag /e /q` returns nothing (no failures) except documented noise.

## Checked
2026-10-27, against the dcdiag reference page on Microsoft Learn (windowsserverdocs, current). Confirmed: switches /s /e /a /c /q /v /f /test /fix; per-test descriptions and look-back windows (SystemLog 60 minutes, KccEvent 15 minutes, DFSREvent and FrsEvent 24 hours, Replications 12-hour latency); MachineAccount repair options; the DNS sub-tests and that /test:DNS defaults to /DnsAll and is not run by default; Services list. Removed as unconfirmed: the FsmoCheck test name, the 15-minute post-reboot figure and the DCOM 10016 example. Corrected: MachineAccount is fixed by /fixmachineaccount, not netdom resetpwd; /test:dns without /e (not without /dnsall) limits the scope to one DC.

Method: documentation only; no commands were run.
