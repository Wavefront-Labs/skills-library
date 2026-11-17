---
id: computing-software.cybersecurity-defensive.network-defence.honeytokens-and-honey-accounts
name: honeytokens-and-honey-accounts
category: computing-software
field: cybersecurity-defensive
product: network-defence
tags: [deception-technology, honeytokens, honey-accounts, decoy-credentials, fake-spn, kerberoasting-detection, decoy-documents, aws-honey-keys]
level: practitioner
status: draft
description: "Plant honeytokens (fake AD accounts and SPNs, decoy credentials, fake AWS keys, decoy files) and alert on any use as a near-zero false-positive detection."
sources: ["MITRE D3FEND Decoy User Credential (D3-DUC) and Decoy File (D3-DF)", "CompTIA Security+ SY0-701 objective 1.2 (honeytoken)", "Microsoft Learn - Defender for Identity honeytoken entity tags"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Honeytokens and honey accounts

**Goal:** fake credentials and objects that only an attacker would find and use, so their use
triggers an alert with almost no false positives.

## Types and detection
| Honeytoken | Plant | Alert on |
|---|---|---|
| Honey AD user | Enabled account, believable name (`svc_backup_old`), never used, strong password, no rights | Any 4624/4625/4768/4771 for the account; Defender for Identity honeytoken tag alerts on authentication |
| Fake SPN (Kerberoasting decoy) | SPN on the honey account (`MSSQLSvc/sql-legacy.corp.example.com:1433`) | 4769 for that SPN (someone requested a ticket = Kerberoasting) |
| Decoy credentials in memory/files | Credentials in a script, `unattend.xml`, browser store or LSASS via logon with fake creds | Use of those credentials anywhere |
| AWS honey keys | Access key for an IAM user with no permissions, left in a config file | CloudTrail any API call with that key ID (even denied) |
| Decoy documents | `Passwords.xlsx` with a canary token (web bug / DNS callback) | Opened document calls back |
| Database honey records | Fake customer row with unique email | Email receives mail (data was stolen and used) |

## Practice
- Make them findable on attacker paths: AD enumeration, file shares, Git repos, admin workstations.
- Document every honeytoken in a restricted register so defenders do not "clean them up" and IR knows them.
- Alert routing: straight to SOC, high priority, include source host/IP.

## Example detection (SPL)
```
index=wineventlog (EventCode=4769 Service_Name="svc_backup_old") OR (EventCode IN (4624,4625,4768,4771) user="svc_backup_old")
```

## Gotchas
- Honey accounts with any real privileges are a liability; give none.
- Some IT tools enumerate and touch all accounts (identity governance, password audits); exclude by source after validation.
- Password must be strong: a cracked honeytoken password is fine (that is the alert) but an easily guessed one invites spraying noise.

## Verify
- [ ] Test authentication with each honey credential raises an alert end to end.
- [ ] Register reviewed quarterly; tokens still present and alerting.
