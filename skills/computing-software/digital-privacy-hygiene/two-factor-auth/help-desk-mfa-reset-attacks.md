---
id: computing-software.digital-privacy-hygiene.two-factor-auth.help-desk-mfa-reset-attacks
name: help-desk-mfa-reset-attacks
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, helpdesk-mfa-reset-attack, social-engineering, account-recovery, scattered-spider]
level: practitioner
status: docs-checked
description: "Understand how attackers use help desks, push bombing and SIM swaps to defeat MFA (CISA AA23-320A on Scattered Spider) and which mitigations the advisory actually lists."
sources:
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Help-desk MFA reset attacks

**Goal:** the human support channel does not become the easiest way around strong authentication.

## How it works (CISA AA23-320A)
Scattered Spider (UNC3944, Octo Tempest, Storm-0875, Muddled Libra) targets large companies and their contracted IT help desks. The advisory was issued November 2023 and updated 29 July 2025.
- Help-desk social engineering: impersonating employees or IT staff by phone or SMS to get password resets or MFA transferred; targets are researched via business sites, social media, leaked data and purchased credentials.
- MFA abuse: push bombing, persuading employees to share one-time passcodes, and having help desk staff move MFA to attacker-controlled devices.
- SIM swapping: persuading carriers to move a number to the attackers' SIM.
- Persistence: registering their own MFA tokens, adding a federated identity provider to the SSO tenant with automatic account linking, creating new identities.

## Mitigations the advisory lists
- Phishing-resistant MFA (FIDO/WebAuthn or PKI-based) for all services where possible, especially webmail, VPNs and critical systems; these resist push bombing and SIM swaps.
- Unique, random passwords of at least 15 characters (including service and admin accounts), a vetted password manager, lockouts after repeated failures, no password hints, no forced periodic changes.
- Enhanced monitoring for risky logins and unusual sign-in behaviour.
- Application allowlisting and auditing of remote access tools; remote access only via approved channels (VPN, VDI); restrict RDP.
- Training against vishing and spearphishing; external-email banners.
- Segmentation, EDR, patching, and tested offline, immutable backups.

## Not in the advisory
The advisory does not recommend help-desk identity-verification procedures; source those elsewhere (for example your identity provider's guidance). Personal measures such as carrier PINs, account notes and verbal passwords are common practice but are not backed by the cited page.

## Gotchas
- Recovery questions answerable from public records are weak; random answers are a reasonable choice (judgement).

## Checked
Method: 2026-11-08 read the full CISA AA23-320A advisory page. TTP and mitigation lists follow it. Removed: the table of per-account personal defences, claims about Google/Apple/Microsoft having no support reset, attackers calling after breach notifications, and the NIST 800-63B source (not read for this skill).
