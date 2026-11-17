---
id: computing-software.cybersecurity-defensive.identity-access-management.mfa-reset-help-desk-verification
name: mfa-reset-help-desk-verification
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [mfa, mfa-reset-process, help-desk, identity-verification, social-engineering, temporary-access-pass, account-recovery]
level: practitioner
status: draft
description: "Run MFA resets and account recovery without becoming the social-engineering bypass: identity proofing at the help desk, temporary access passes, approvals and monitoring."
sources: ["https://pages.nist.gov/800-63-4/sp800-63b.html", "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a", "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# MFA reset and help-desk identity verification

**Goal:** a user who lost their phone or key gets back in quickly, while an attacker calling
the help desk pretending to be that user does not. Help-desk MFA resets were the entry point
in several major intrusions (e.g. Scattered Spider, CISA AA23-320A).

## Verification ladder (stronger first)
1. **Self-service with remaining strong factor:** user still has another registered
   phishing-resistant method (second security key, passkey on another device) and re-registers.
2. **Manager or colleague vouching in person / on a verified video call** with photo ID
   compared against HR records.
3. **In-person ID check** at an office or by a trusted local contact.
4. **Identity verification service** (document + liveness check, e.g. Entra Verified ID
   with a verification partner) for remote staff.
Avoid knowledge-based questions (birth date, manager name, employee ID) and callback to
numbers supplied by the caller; all are researchable or controllable by attackers. Call back
on the number from the HR system only, and treat even that as weak for privileged users.

## Issue a time-limited credential, not a permanent bypass
- Entra **Temporary Access Pass** (TAP): one-time or short lifetime (e.g. 1 hour), used to
  register new methods; Okta has a similar one-time recovery flow.
- Never disable MFA for the user "temporarily" or set a known password over the phone.

## Extra controls for privileged and high-risk users
- Two-person rule: second help-desk agent or security approves resets for admins, executives,
  finance roles.
- Resets for privileged accounts only in person or via the strongest method; tier-0 admins'
  recovery handled by the identity team, not the general help desk.

## Monitoring
Alert on: MFA method registration and deletion events, TAP creation, resets for privileged
accounts, multiple resets by one agent in a short time, sign-ins from new devices/locations
right after a reset. Notify the user through an existing channel (email to manager, push to
old device) when their methods change.

## Gotchas
- Help-desk agents measured on call time skip verification; give them a script and backing to refuse.
- Outsourced help desks need the same procedure and audit.
- Users with only one registered method create frequent resets; require two methods at registration.

## Verify
Quarterly social-engineering test calls to the help desk (authorised) using public
information only; resets must fail without passing the ladder. Audit a sample of resets for
recorded verification evidence.
