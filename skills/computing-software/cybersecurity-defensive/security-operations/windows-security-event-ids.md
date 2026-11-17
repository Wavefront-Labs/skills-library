---
id: computing-software.cybersecurity-defensive.security-operations.windows-security-event-ids
name: windows-security-event-ids
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [log-analysis, windows-event-ids, security-evtx, 4624, 4625, 4688, 4720, 4672, logon-types, kerberos-events, event-log-analysis]
level: practitioner
status: docs-checked
description: "Read Windows Security log event IDs that matter in investigations: logon types, process creation, account and group changes, Kerberos and log clearing."
sources: ["https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4688", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4768", "https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-1102"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Security event IDs for investigation

**Goal:** know which events answer which question, and what the key fields mean, so you
read logs quickly and do not over- or under-interpret them.

## Logons (on the target machine)
| ID | Meaning | Key fields |
|---|---|---|
| 4624 | Successful logon: a logon session was created on the destination machine | Logon Type, account name, source network address, workstation name, logon process, authentication package |
| 4625 | Failed logon, logged for any logon failure; on DCs, member servers and workstations | Status / Sub Status (0xC000006A bad password, 0xC0000064 bad user name, 0xC0000234 account locked out) |
| 4634 / 4647 | Logoff (4634 session terminated; 4647 user-initiated logoff) | Logon ID: correlate with the 4624 of the same Logon ID |
| 4648 | A process attempted a logon by explicitly specifying an account's credentials | Compare target server and process; seen with runas and remote tooling |
| 4672 | Special (sensitive) privileges assigned to a new logon session | Marks privileged logons |

Logon types (4624 and 4625): 2 Interactive, 3 Network, 4 Batch, 5 Service, 7 Unlock, 8 NetworkCleartext
(password handed to the authentication package unhashed; built-in packages still hash before sending),
9 NewCredentials (cloned token with new outbound credentials), 10 RemoteInteractive (Terminal Services / RDP),
11 CachedInteractive (cached credentials, DC not contacted). Microsoft also lists 12 and 13 on the 4624 page.
Monitor Logon Type 4 or 5 used by members of administrative groups.

## Domain controller events
| ID | Meaning |
|---|---|
| 4768 | Kerberos TGT issued (DCs only). Ticket encryption type 0x17 is RC4-HMAC, the default suite only for operating systems before Windows Server 2008 / Vista |
| 4769 | Kerberos service ticket (TGS) requested (DCs only). Review unusual volumes of RC4 requests across many service names from one account (analyst heuristic, not stated by Microsoft) |
| 4771 | Kerberos pre-authentication failed (KDC could not issue a TGT: wrong or expired password). Not generated for accounts with "Do not require Kerberos preauthentication" |
| 4776 | NTLM credential validation, logged on the authoritative computer (DC for domain accounts); also fires on workstation unlock |
| 4720 / 4726 | User object created / deleted |
| 4732 | Member added to a security-enabled local group |
| 4738 | User object changed |
| 5136 | Active Directory object modified (needs the Audit Directory Service Changes subcategory) |

## Process and persistence
| ID | Meaning |
|---|---|
| 4688 | Process created. Command line is empty by default; enable the group policy "Include command line in process creation events" (Administrative Templates > System > Audit Process Creation) |
| 4697 | Service installed (Security log) |
| 4698 | Scheduled task created |
| 1102 | Security audit log cleared (treat as an alert) |
| 4719 | Computer audit policy changed (always logged regardless of the Audit Policy Change subcategory setting) |

## Query examples (illustrative; table and field names depend on your ingestion)
KQL (Sentinel `SecurityEvent`): `SecurityEvent | where EventID == 4625 | summarize count() by TargetAccount, IpAddress, bin(TimeGenerated, 10m) | where count_ > 20`
SPL: `index=wineventlog EventCode=4624 Logon_Type=10 | stats count by user src_ip dest`

## Gotchas
- Events only exist if the audit policy enables them; absence of 4688 often means not audited, not "no process ran".
- Baseline normal Network (type 3) logons before alerting on them.
- Compare the source network address and workstation name against where the account should be used from.
- Forward logs centrally so log clearing (1102) does not destroy the only copy.

## Verify
- [ ] For each investigation question, the relevant event ID is confirmed audited on the in-scope hosts.
- [ ] Interpretations of logon type and status codes cited in the case notes.

## Checked
Checked 2026-11-08 against the Microsoft Learn event pages for 4624, 4625, 4634, 4647, 4648, 4672, 4688, 4697, 4698,
4719, 4720, 4726, 4732, 4738, 4768, 4769, 4771, 4776, 5136 and 1102. Confirmed: event meanings, logon type table,
status codes 0xC000006A / 0xC0000064 / 0xC0000234, 0x17 RC4-HMAC, the 4688 command-line policy and its empty
default, 4719 always logged, 5136 subcategory. Removed because not confirmed on fetched pages (4728 and 4756 pages
returned 404): IDs 4728, 4756 and System 7045, the 20 MB default log size, the IIS basic auth remark on type 8,
the "DC to every host is normal" claim, and the Kerberoasting, password spraying and lateral-movement labels
(now marked as heuristics or dropped).
Method: documentation only; no commands were run.
