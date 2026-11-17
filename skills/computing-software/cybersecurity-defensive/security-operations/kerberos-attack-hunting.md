---
id: computing-software.cybersecurity-defensive.security-operations.kerberos-attack-hunting
name: kerberos-attack-hunting
category: computing-software
field: cybersecurity-defensive
product: security-operations
tags: [threat-hunting, kerberos-attack-hunting, kerberoasting, as-rep-roasting, golden-ticket, silver-ticket, event-4769, event-4768, rc4-tickets]
level: advanced
status: docs-checked
description: "Hunt Kerberos abuse in DC logs: Kerberoasting via RC4 4769 bursts, AS-REP roasting, golden and silver ticket anomalies, delegation abuse, and decoy SPNs."
sources: ["https://attack.mitre.org/techniques/T1558/", "https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4769", "https://adsecurity.org/?p=3458"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos attack hunting

Prerequisite: Kerberos authentication and service ticket auditing (Success and Failure) on all DCs, logs centralised.

## Kerberoasting (T1558.003)
Attacker requests service tickets for SPN accounts, cracks them offline. Signal in 4769:
- `TicketEncryptionType` `0x17` (RC4) when your environment uses AES (`0x12`).
- One account requesting tickets for many distinct services in minutes.
- Service names that are user accounts (not `krbtgt`, not computer accounts ending `$`).
```kql
SecurityEvent
| where EventID == 4769 and TicketEncryptionType == "0x17"
| where ServiceName !endswith "$" and ServiceName != "krbtgt"
| summarize services=dcount(ServiceName) by TargetUserName, IpAddress, bin(TimeGenerated, 10m)
| where services > 5
```
Decoy: create an SPN on an unused account with a long random password; any 4769 for it is malicious.

## AS-REP roasting (T1558.004)
Accounts configured to skip Kerberos pre-authentication. Hunt 4768 events for those accounts, and audit the configuration too: the list should be empty.

## Golden ticket (T1558.001)
Forged TGT with the krbtgt key. Indicators:
- 4769 (service ticket) with no preceding 4768 (TGT) from that client in the ticket lifetime.
- Ticket lifetimes beyond policy - visible to Defender for Identity / Kerberos traffic analysis, not in standard events.
- Account names that do not exist or RID/name mismatches; domain field oddities (lowercase,
  FQDN vs NetBIOS).

## Silver ticket (T1558.002)
Forged service ticket with a service account/computer key; never touches the DC, so DC logs show
nothing. Detect on the target host: 4624/4634 logons with no corresponding DC 4769, PAC validation
failures. Mitigate with AES-only and regular computer password rotation.

## Delegation abuse
- Unconstrained delegation hosts receiving TGTs of privileged users (printer bug coercion):
  hunt 4624 from DCs to non-DC hosts plus spooler/EFS RPC calls.
- Resource-based constrained delegation: hunt for changes to the delegation attribute on computer accounts, then unusual service ticket requests.

## Gotchas
- Legacy apps legitimately use RC4; inventory and fix them (or exclude precisely) to make RC4 a
  clean signal.
- 4769 volume is enormous; aggregate at the DC/forwarder or in summary tables.

## Verify
In a lab, run a Kerberoast tool (e.g. Rubeus kerberoast in a test domain) and confirm the
4769 burst query and decoy SPN alert both fire.

## Checked

Date: 2026-10-28

- Confirmed: Kerberoasting uses service tickets with RC4_HMAC_MD5 encrypted by the service account hash (adsecurity.org); 4769 fields TicketEncryptionType, ServiceName, IpAddress, TargetUserName (SecurityEvent table); technique IDs T1558.001-004 (MITRE ATT&CK); krbtgt password rotation guidance.
- Removed (not found): make_set aggregation, PreAuthType field name, Get-ADUser filter, Mimikatz 10 year lifetime and default 10h policy, msDS-AllowedToActOnBehalfOfOtherIdentity and S4U detail, RC4 phase-out claim, exact audit subcategory and flag names.
Method: documentation only; no commands were run.

