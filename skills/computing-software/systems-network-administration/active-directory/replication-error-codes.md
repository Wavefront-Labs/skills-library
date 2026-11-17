---
id: computing-software.systems-network-administration.active-directory.replication-error-codes
name: replication-error-codes
category: computing-software
field: systems-network-administration
product: active-directory
tags: [active-directory, ad-replication, replication-error-8614, replication-error-1722, replication-error-8606, replication-error-8453, replication-error-8524, replication-error-1256, replication-error-5, repadmin, troubleshooting]
level: advanced
status: docs-checked
description: "Fix common AD replication errors by code: 1722 RPC unavailable, 5 access denied, 8453, 8524 DNS, 8606/8614 lingering/tombstone, 1256 and 1908."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-1722-rpc-server-unavailable
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8614
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8524
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replications-fail-with-error-5
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8453
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8456-8457
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-8606
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/replication-error-1753
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/active-directory-replication-error-8451
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/ad-replication-error-1908-not-find-domain-controller
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/active-directory/active-directory-replication-error-1256
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AD replication errors by code

Get the code from `repadmin /showrepl <dc>` or `/replsummary`, then:

| Code | Meaning | Usual cause | Fix |
|---|---|---|---|
| **1722** | RPC server unavailable | firewall, partner down, DNS points to wrong IP, RPC ports blocked, SMB signing mismatch, bad NIC driver | `portqry -n <partner> -e 135`; check the A record matches the partner's IP; check the firewall allows the RPC endpoint mapper and dynamic ports |
| **1256** | remote system not available | partner unreachable at network level | same as 1722, check routing/VPN |
| **1753** | no more endpoints | RPC endpoint mapper reachable but the server app never registered (failed start or died), or the name resolves to a different server | check the partner's health and the DNS name-to-IP mapping |
| **5** | access denied | secure channel or password mismatch, time skew (Kerberos allows 5 minutes), `RestrictRemoteClients` = 2, `CrashOnAuditFail` = 2, SMB signing mismatch, broken trust | `nltest /sc_query:<domain>`; `netdom verify <DC>`; `netdom resetpwd /server:<dc> /userd:<DOMAIN>\<admin> /passwordd:*`; `w32tm /monitor` and fix time |
| **8453** | replication access denied | missing *Replicating Directory Changes* rights; top cause is an RODC destination where *Enterprise Read-Only Domain Controllers* lacks the right on the NC root; also invalid UserAccountControl or default security descriptors | grant the right on the NC head; `dcdiag /test:CheckSecurityError` |
| **8524** | DSA operation unable to proceed because of a DNS lookup failure | partner's `<guid>._msdcs` CNAME missing/stale | `dcdiag /test:dns`; `ping <guid>._msdcs.<forest root domain>`; restart Netlogon on the partner; fix DNS client settings on DCs |
| **8606** | insufficient attributes to create an object | source sends an update for an object already deleted and garbage-collected on a strict-consistency destination (lingering object) | remove lingering objects (`repadmin /removelingeringobjects`) |
| **8614** | time since last replication exceeded tombstone lifetime | DC isolated longer than the tombstone lifetime, or its clock jumped forward by that much | check for lingering objects first, then (if acceptable) set `Allow Replication With Divergent and Corrupt Partner` (`repadmin /regkey <DC> +allowDivergent`), or demote and rebuild the DC |
| **8451** | replication operation encountered a database error | AD database or index corruption (several root causes) | check hardware, run the Ntdsutil file integrity and semantic database analysis commands, offline defrag, otherwise restore or demote and re-promote |
| **1908** | could not find the domain controller | destination cannot contact a KDC, or Kerberos errors | `nltest /dsgetdc:<domain>` from the destination |
| **8456 / 8457** | source/destination rejecting replication | replication disabled by the OS (USN rollback, full disk, corrupt UTD vector) or by an admin | read the `DSA not writable` value under `HKLM\SYSTEM\CurrentControlSet\Services\NTDS\Parameters` and events 2103, 1393, 2881; investigate before re-enabling |

## Method
1. Identify direction: error on destination D pulling from source S.
2. Test S from D: name resolution, RPC (135 and dynamic ports), SMB, LDAP, Kerberos, time, secure channel.
3. Fix root cause, then `repadmin /replicate D S <NC>` and recheck.

## Verify
- [ ] `repadmin /replsummary` zero fails after fix.
- [ ] Root cause recorded (firewall change, DNS record, isolated DC) to prevent recurrence.

## Checked
2026-10-27, against the Microsoft Learn troubleshooting article for each code (SupportArticles-docs, current pages). Confirmed per code (including w32tm /monitor for time checks): error text and causes for 1722, 1256, 1753, 5 (causes and netdom/nltest commands), 8453 (RODC and Enterprise Read-Only Domain Controllers), 8524 (_msdcs CNAME lookup), 8606, 8614 (including allowDivergent and the clock-jump cause), 8451, 1908, 8456/8457 (DSA not writable values and events 2103, 1393, 2881). Removed as unconfirmed: the 49152-65535 range, Test-NetConnection, ipconfig /registerdns, repadmin /options, the 8456 admin-disabled command.

Method: documentation only; no commands were run.
