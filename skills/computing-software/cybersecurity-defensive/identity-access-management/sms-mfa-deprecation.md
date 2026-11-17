---
id: computing-software.cybersecurity-defensive.identity-access-management.sms-mfa-deprecation
name: sms-mfa-deprecation
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [sms-mfa-deprecation, sms-mfa, voice-mfa, sim-swap, authentication-methods-policy, nist-800-63b, mfa]
level: practitioner
status: docs-checked
description: "Phase out SMS and voice MFA: why they are restricted (SIM swap, interception), migration campaigns, authentication methods policy changes, and handling exceptions."
sources: ["https://pages.nist.gov/800-63-4/sp800-63b.html", "https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-methods-manage", "https://www.cisa.gov/sites/default/files/2023-01/fact-sheet-implementing-phishing-resistant-mfa-508c.pdf"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SMS and voice MFA deprecation

NIST SP 800-63B sets specific requirements for PSTN (SMS/voice) out-of-band authenticators (see its PSTN
sections). Threats: SIM swap/port-out fraud, SS7 interception,
phishing relay, number recycling.

## Plan
1. **Measure:** authentication methods activity report - users whose only/default method is SMS or voice.
2. **Offer better:** Microsoft Authenticator push with number matching, passkeys/FIDO2, Windows Hello.
3. **Campaign:** registration campaign nudges, comms, help desk desk-side support; deadlines per department.
4. **Policy change (Entra):** move to the converged Authentication methods policy (legacy MFA and SSPR policies migrated), remove SMS/voice from the enabled methods for the target groups, keep for an exception group.
5. **SSPR:** remove phone methods from SSPR too, or attackers use SIM swap to reset passwords.
6. **Exceptions:** users without smartphones get FIDO2 keys or OATH hardware tokens rather than SMS.
7. **Monitor** the exception group size and expire exceptions.

## Gotchas
- SMS as "backup method" still lets an attacker pick it at sign-in; remove it, not just change the default.
- Privileged roles should already be on phishing-resistant methods only (authentication strength).
- Customer-facing apps: offer passkeys first; keep SMS as a risk-managed fallback with fraud controls (port-out checks, velocity limits).

## Verify
- [ ] Authentication methods policy shows SMS/voice disabled for all but the exception group.
- [ ] Sign-in logs: SMS-satisfied MFA count trending to zero.

## Checked

2026-10-28. Confirmed against the Entra authentication methods management page: converged Authentication methods policy replacing the legacy MFA and SSPR policies; NIST SP 800-63B PSTN sections exist. Removed: the specific wording 'restricted, only with risk acceptance and alternative offered' (check the current SP 800-63B text), Okta Verify mention.

Method: documentation only; no commands were run.
