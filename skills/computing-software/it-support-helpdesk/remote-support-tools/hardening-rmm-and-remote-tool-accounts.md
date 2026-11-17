---
id: computing-software.it-support-helpdesk.remote-support-tools.hardening-rmm-and-remote-tool-accounts
name: hardening-rmm-and-remote-tool-accounts
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, rmm-hardening, rmm, mfa, least-privilege, screenconnect, audit-log, privileged-access]
level: practitioner
status: draft
description: "Lock down RMM and remote-support consoles: SSO and phishing-resistant MFA, RBAC, IP restriction, script approval, audit to SIEM, and fast patching of exposed servers."
sources:
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-025a"
  - "https://www.cisa.gov/news-events/alerts/2024/02/22/cisa-adds-one-known-exploited-connectwise-vulnerability-cve-2024-1709-catalog"
  - "https://www.cisa.gov/news-events/news/kaseya-ransomware-attack-guidance-affected-msps-and-their-customers"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# hardening-rmm-and-remote-tool-accounts

An RMM console is a remote shell on every endpoint at once. Treat it like domain admin.

## Accounts
- SSO to the identity provider with phishing-resistant MFA (FIDO2/passkeys); no local
  console accounts except one break-glass account in a vault.
- Named accounts only; no shared "support" logins.
- Disable accounts in the same leaver workflow as email (see disabling-accounts-and-revoking-sessions).

## Permissions
- RBAC: L1 gets remote control and view on their client groups; script execution and
  policy edit go to fewer people.
- Unattended access requires a ticket reference or approval where the tool supports it.
- Remove "run any script as SYSTEM" from roles that do not need it; use an approved
  script library with review (see script-safety-and-review).

## Exposure
- Self-hosted servers (ScreenConnect, Automate, VSA): patch within days of critical
  advisories. ScreenConnect CVE-2024-1709 (auth bypass, fixed in 23.9.8) was mass-exploited
  within days; the 2021 Kaseya VSA attack pushed ransomware through the RMM itself.
- Restrict console access by IP or behind ZTNA where possible.
- Rotate API keys and integration tokens; scope them minimally.

## Monitoring
- Send console audit logs (logins, sessions, scripts run, policy changes) to the SIEM.
- Alert on: new admin created, MFA removed, script pushed to all devices, logins from new
  countries, sessions outside business hours without a ticket.

## Gotchas
- Free trial tenants of the same RMM are an attacker favourite; block unknown tenant IDs
  (see detecting-unapproved-remote-access-tools).
- Agent install links left public let anyone enrol devices into your console.

## Verify
Quarterly review: every console account maps to a current staff member with MFA, roles
match job, audit logs arrive in the SIEM, and server version is current.
