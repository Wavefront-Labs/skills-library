---
id: computing-software.digital-forensics-incident-response.incident-response-process.running-an-enterprise-password-reset-campaign
name: running-an-enterprise-password-reset-campaign
category: computing-software
field: digital-forensics-incident-response
product: incident-response-process
tags: [password-reset-campaign, eradication, account-containment, krbtgt-reset, dfir]
level: advanced
status: draft
description: "Plan an enterprise-wide password reset after credential compromise: ordering, privileged accounts first, service accounts, comms, helpdesk load and verification."
sources: ["https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks", "https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/forest-recovery-guide/ad-forest-recovery-reset-the-krbtgt-password", "https://www.cisa.gov/stopransomware/ransomware-guide"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Running an enterprise password reset campaign

**Goal:** invalidate every credential the attacker may hold (from LSASS dumps, NTDS.dit theft,
DCSync or phishing) in an order that does not leave them a way back in.

## Before the reset
- Eradicate footholds first; resetting passwords while malware with keyloggers or credential
  dumpers is still running just hands over new passwords.
- Inventory: privileged accounts, break-glass accounts, service accounts (and where their
  passwords are stored), shared/generic accounts, local admin passwords (LAPS?), cloud-only admins.

## Order
1. Attacker-created and suspect accounts: disable.
2. Tier 0: domain/enterprise admins, AD CS admins, Entra global admins, backup admins - new
   passwords set from a clean admin workstation, MFA re-registered.
3. **krbtgt twice**, with replication-complete interval between (at least 10 h, or the max
   ticket lifetime) to invalidate golden tickets.
4. Service accounts: rotate in coordination with application owners; move to gMSA where possible.
5. Local admin passwords: deploy/rotate Windows LAPS on all hosts.
6. All users: force change at next logon (`pwdLastSet = 0`) in waves by OU, and revoke cloud
   sessions/refresh tokens (`Revoke-MgUserSignInSession`).
7. Machine accounts of compromised hosts: reset or rejoin.

## Operations
- Helpdesk surge staffing and an identity-verification script (callback) to defeat social engineering.
- Comms to users through a channel the attacker cannot spoof; explain they will never be asked
  for passwords by email.
- Hybrid: confirm password hash sync / writeback timing; synced users may keep old cloud tokens
  until revoked.

## Verify
- `Get-ADUser -Filter * -Properties pwdLastSet` shows all in-scope accounts after the campaign start time.
- Monitor 4625/4771 for old-password attempts from unusual sources: these are the attacker.

## Gotchas
- Forgetting non-AD credentials: VPN local users, network devices, hypervisors, SaaS admins, API keys.
- Resetting a service account without updating every server that uses it causes outages.
