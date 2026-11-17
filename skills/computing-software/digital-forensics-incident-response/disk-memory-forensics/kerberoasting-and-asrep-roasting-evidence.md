---
id: computing-software.digital-forensics-incident-response.disk-memory-forensics.kerberoasting-and-asrep-roasting-evidence
name: kerberoasting-and-asrep-roasting-evidence
category: computing-software
field: digital-forensics-incident-response
product: disk-memory-forensics
tags: [kerberoasting, asrep-roasting, credential-theft, 4769, kerberos, active-directory, dfir]
level: practitioner
status: draft
description: "Detect Kerberoasting and AS-REP roasting in domain controller logs: 4769 RC4 service ticket bursts, 4768 without pre-auth, tooling artefacts and exposed accounts."
sources: ["https://attack.mitre.org/techniques/T1558/003/", "https://attack.mitre.org/techniques/T1558/004/", "https://adsecurity.org/?p=3458"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Kerberoasting and AS-REP roasting evidence

**Goal:** determine whether service account or no-preauth account hashes were requested for
offline cracking, and which accounts must be rotated.

## Kerberoasting (T1558.003)
- DC Security **4769** (service ticket requested): `TicketEncryptionType` **0x17 (RC4)**
  for services that support AES, `ServiceName` = user accounts with SPNs (not `krbtgt` or
  computer `$` accounts), many distinct services requested by one account in a short time,
  `TicketOptions` 0x40810000 typical of tooling.
- Tools: Rubeus `kerberoast`, Impacket `GetUserSPNs.py`, PowerView `Invoke-Kerberoast`;
  source-host artefacts (4104 script block, Prefetch, LDAP queries for
  `servicePrincipalName=*` in LDAP client/DS logs or EDR LDAP telemetry).
```kusto
SecurityEvent | where EventID == 4769 and TicketEncryptionType == "0x17"
| where ServiceName !endswith "$" and ServiceName != "krbtgt"
| summarize Services = dcount(ServiceName), make_set(ServiceName) by TargetUserName, IpAddress, bin(TimeGenerated, 10m)
| where Services > 5
```

## AS-REP roasting (T1558.004)
- Accounts with "Do not require Kerberos preauthentication" (`DONT_REQ_PREAUTH`); DC
  **4768** with `PreAuthType` **0** for those accounts, often RC4, from unusual IPs.
- Find exposed accounts: `Get-ADUser -Filter 'useraccountcontrol -band 4194304' -Properties useraccountcontrol`.

## Response
Treat requested accounts as cracked if passwords are weak: rotate to long random passwords
(25+ chars) or gMSA, enable AES-only, remove unnecessary SPNs, re-enable pre-auth. Check
whether the account was later used (4624 from new hosts).

## Gotchas
- Some legacy apps legitimately request RC4; baseline first.
- Honeypot SPN accounts (decoy) make detection near-certain; consider deploying one.

## Verify
List of roasted accounts, request times, source IP/host, and rotation completion recorded.
