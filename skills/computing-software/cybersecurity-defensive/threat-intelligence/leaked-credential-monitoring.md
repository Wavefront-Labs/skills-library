---
id: computing-software.cybersecurity-defensive.threat-intelligence.leaked-credential-monitoring
name: leaked-credential-monitoring
category: computing-software
field: cybersecurity-defensive
product: threat-intelligence
tags: [digital-risk-protection, credential-leak-monitoring, hibp, infostealer-logs, combolists, password-reset, account-takeover]
level: practitioner
status: draft
description: "Monitor for leaked corporate and customer credentials from breaches and infostealer logs, validate exposure, force resets and revoke sessions, and protect against credential stuffing."
sources: ["Have I Been Pwned - Domain search and API documentation", "Microsoft Entra ID Protection - Leaked credentials detection", "NIST SP 800-63B section 5.1.1.2 - check passwords against breached corpuses"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Leaked credential monitoring

**Goal:** detect corporate (and customer) credentials exposed in breaches, combolists or infostealer logs and neutralise them before use.

## Sources
- Have I Been Pwned domain search (verified domain owners get notifications for addresses in breaches).
- Microsoft Entra ID Protection "Leaked credentials" risk detection (Entra ID P2, with password hash sync).
- Commercial DRP/threat intel (infostealer log marketplaces, Telegram channels, combolists) - Recorded Future, Flare, SpyCloud, Hudson Rock and others.
- Internal: password filters checking breached corpuses (Pwned Passwords k-anonymity API, Entra Password Protection banned lists, Specops/Lithnet for on-prem AD).

## Infostealer logs matter most
They include URL + username + password + session cookies + device info from an infected machine (often a personal device used for work). Session cookies bypass MFA.

## Response playbook
1. Validate: is the account real and active? Is the credential current (same password? check without testing logins against production - use hash comparison where provider supports it)?
2. Force password reset; **revoke sessions and refresh tokens** (`Revoke-MgUserSignInSession`, Okta clear sessions); review MFA methods for attacker-added devices.
3. Review sign-in logs since exposure date for suspicious access.
4. Infostealer case: identify the infected device (log includes hostname/IP); if corporate, isolate and reimage; if personal, advise user and enforce compliant-device access.
5. Customer credentials: forced reset at next login, notify per policy, watch for credential stuffing against login APIs (rate limits, bot detection).

## Prevention
Phishing-resistant MFA, conditional access requiring compliant devices, short session lifetimes for sensitive apps, token protection/binding where available, banning breached passwords.

## Verify
- [ ] Domain is registered with HIBP and alerts route to the SOC queue.
- [ ] Playbook includes session revocation, not just password reset.
