---
id: computing-software.it-support-helpdesk.remote-support-tools.help-desk-social-engineering-defence
name: help-desk-social-engineering-defence
category: computing-software
field: it-support-helpdesk
product: remote-support-tools
tags: [it-support-helpdesk, remote-support-tools, help-desk-social-engineering, mfa-reset-attack, identity-verification, vishing, scattered-spider, caller-verification]
level: advanced
status: draft
description: "Stop attackers who phone the help desk for password and MFA resets: verification that resists impersonation, high-risk request rules, red flags, and response."
sources:
  - "https://www.cisa.gov/news-events/cybersecurity-advisories/aa23-320a"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/howto-authentication-temporary-access-pass"
  - "https://www.microsoft.com/en-us/security/blog/2023/10/25/octo-tempest-crosses-boundaries-to-facilitate-extortion-encryption-and-destruction/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# help-desk-social-engineering-defence

Groups like Scattered Spider / Octo Tempest (CISA AA23-320A) breached large companies by
calling the service desk, impersonating employees (often IT staff or executives), and
getting MFA reset or a new device registered. They research names, managers, employee IDs
from LinkedIn and breached data. Knowledge-based questions don't stop them.

## Verification that holds up
Rank methods; high-risk requests need a strong one:
1. **Verified ID in a video call** with a live check against the HR photo, or in person.
2. **Push/number match to an already-registered method** (e.g. Authenticator approval
   initiated from the admin side, or a self-service verification flow).
3. **Call back** on the number in the HR system (not the number the caller gives), or a
   manager vouches through a *separate* channel they initiate.
Weak (never sufficient alone for MFA/device changes): employee ID, date of birth,
manager's name, last four of SSN, office location, anything on LinkedIn.

## High-risk requests (require strong verification and often a second person)
- MFA method reset or new method registration.
- Temporary Access Pass issuance.
- Password reset for admins, executives, finance, IT staff.
- Adding a device, changing phone number, disabling MFA "while travelling".
Policy: these requests can't be completed on an inbound call alone; call back via HR
records or verify by video. Privileged accounts: no help desk reset at all, only via the
identity team with in-person or manager-witnessed verification.

## Red flags
- Urgency and pressure ("I'm presenting to the board in 10 minutes").
- Caller claims to be new, travelling, phone lost, so can't use normal methods.
- Background noise inconsistent, unusual accent for the claimed person, calling from a
  number not in HR records.
- Asks for MFA reset *and* to add a new phone in one call.
- Second call minutes later to another agent after being refused.

## If you suspect an attack
1. Don't complete the request. Be polite: "I'll need to call you back on your registered
   number."
2. Record caller number, time, details claimed; raise a security incident immediately.
3. Security checks the real user's sign-in logs and recent method changes; consider
   revoking sessions and alerting the user.
4. Warn the desk team in real time (the same attacker will try other agents).

## Gotchas
- Self-service reset with SMS as the only method is weak against SIM swap; prefer
  Authenticator/passkeys.
- Agents need management backing to refuse a "VIP" caller; make it explicit in policy.

## Verify
Monthly test calls (red team or vishing simulation) to the desk; agents follow the
verification procedure, and audit of MFA resets shows a recorded strong verification for each.
