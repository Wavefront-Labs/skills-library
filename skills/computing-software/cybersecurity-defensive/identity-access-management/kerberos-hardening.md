---
id: computing-software.cybersecurity-defensive.identity-access-management.kerberos-hardening
name: kerberos-hardening
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sso, kerberos-hardening, active-directory, kerberoasting, aes-encryption, delegation, rc4-deprecation]
level: advanced
status: docs-checked
description: "Harden Kerberos in Active Directory: move to AES and retire RC4, defend against Kerberoasting and AS-REP roasting, lock down delegation, and monitor ticket anomalies."
sources: ["https://learn.microsoft.com/en-us/windows-server/security/kerberos/kerberos-authentication-overview", "https://learn.microsoft.com/en-us/windows-server/security/kerberos/detect-remediate-rc4-kerberos", "https://attack.mitre.org/techniques/T1558/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Kerberos hardening

**Goal:** remove the Kerberos weaknesses attackers use for credential theft and privilege
escalation in AD: weak encryption, roastable accounts and unconstrained delegation.

## 1. Encryption types: AES only
- Audit RC4 usage: DC events 4768/4769 with `Ticket Encryption Type 0x17` (RC4); accounts with
  `msDS-SupportedEncryptionTypes` unset or including RC4.
- Set `msDS-SupportedEncryptionTypes` to AES (0x18) on service accounts and computers; GPO
  *Network security: Configure encryption types allowed for Kerberos* to AES128/AES256 (plus
  Future types) once no RC4 dependencies remain.
- See Microsoft's RC4 detection and remediation article for the current RC4 deprecation timeline;
  finish this before defaults change.

## 2. Kerberoasting (T1558.003)
Any domain user can request service tickets for accounts with SPNs and crack them offline.
- Inventory user accounts with SPNs: `Get-ADUser -Filter {ServicePrincipalName -like "*"} -Properties ServicePrincipalName,PasswordLastSet`.
- Replace with **gMSAs** (automatically rotated passwords) wherever possible.
- Remaining SPN accounts: long random passwords, AES only, least privilege; remove
  SPNs no longer needed; never put SPN accounts in privileged groups.
- Detect: 4769 bursts from one user for many services, RC4 ticket requests, honeypot SPN account.

## 3. AS-REP roasting (T1558.004)
Find accounts with "Do not require Kerberos preauthentication":
`Get-ADUser -Filter {DoesNotRequirePreAuth -eq $true}`; clear the flag.

## 4. Delegation
- **Unconstrained delegation** on anything other than DCs lets a compromised server capture
  TGTs (printer bug/coercion attacks). Find: `Get-ADComputer -Filter {TrustedForDelegation -eq $true}`.
  Replace with constrained or resource-based constrained delegation (RBCD).
- Mark privileged accounts *Account is sensitive and cannot be delegated* and/or add them to
  **Protected Users** (no delegation, no RC4, no NTLM).
- Monitor writes to the resource-based constrained delegation attribute (RBCD abuse).

## 5. KRBTGT and tickets
Rotate the KRBTGT password regularly (twice, with replication between) and after compromise.
Detect golden/silver ticket indicators with ticket lifetime anomalies and Defender for Identity.

## Gotchas
- Legacy apps and non-Windows Kerberos clients (old Linux keytabs, NAS devices) may require
  RC4; regenerate keytabs with AES first.
- Protected Users breaks service accounts and cached logons; for human admins only, test first.

## Verify
4769 events show no RC4 tickets for a week; no user accounts with SPNs and weak/old passwords;
no non-DC unconstrained delegation; BloodHound shows no Kerberoastable paths to tier 0.

## Checked

2026-10-28. Confirmed against the Kerberos pages, MITRE T1558 and T1558.003, and the Protected Users page: 4769 with etype 0x17 (RC4), msDS-SupportedEncryptionTypes value 24 (0x18) = AES128 and AES256, Protected Users blocks NTLM, DES/RC4 and delegation, 'Account is sensitive and cannot be delegated', KRBTGT reset twice. Removed: 120-char gMSA figure, 25+ character figure, 4-hour TGT figure, RBCD attribute name, AES-key password reset claim, RC4 default-change claim.

Method: documentation only; no commands were run.
