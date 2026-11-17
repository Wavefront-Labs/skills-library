---
id: computing-software.digital-privacy-hygiene.two-factor-auth.responding-to-push-bombing
name: responding-to-push-bombing
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, push-bombing, mfa-fatigue, push-notifications, number-matching, password-compromise, deny-and-report, microsoft-authenticator]
level: intro
status: docs-checked
description: "When you get a stream of sign-in approval prompts you did not trigger, deny them all, treat the password as compromised, and prefer number matching or phishing-resistant MFA."
sources:
  - "https://www.cisa.gov/sites/default/files/publications/fact-sheet-implement-number-matching-in-mfa-applications-508c.pdf"
  - "https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-mfa-number-match"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Responding to push bombing

**What it is (CISA):** push bombing or MFA fatigue is an attacker who already has your password triggering mobile push prompts, possibly hundreds in a short time, until you approve one by accident, from annoyance, or because you assume one is legitimate.

## Immediately
1. Deny every prompt; do not approve to make it stop.
2. Tell your IT security team (at work) so they can investigate the root cause. CISA: MFA checks come after the first factor, so denied requests could mean your password is compromised.
3. Change that account's password from a known-good device (judgement: standard response, not stated in the sources) and review recent activity.

## Find the cause
CISA lists how passwords get obtained: password spraying, a dump from a compromised site, or other methods. Fix that cause, or the attacker can return.

## Harden
- CISA's first recommendation is phishing-resistant MFA (FIDO/WebAuthn, PKI-based), which it rates as resistant to push bombing. Number matching is "not as strong" but one of the best interim mitigations.
- Number matching makes you enter a number shown on the login screen into the app. You cannot approve without seeing the login screen, and each prompt carries its own numbers, so spamming prompts does not work.
- Vendors name it differently: Microsoft number matching, Duo Verified Push, Okta TOTP.
- Microsoft Authenticator (Entra): number matching is enabled for all Authenticator push notifications; users cannot opt out; older Authenticator versions cannot sign in; Apple Watch and wearables cannot approve (use the phone). On the same device as Authenticator, Microsoft mobile apps (Outlook, Teams) may show Approve/Deny, but browsers still require typing the number.
- For organisations: train users to recognise and report MFA spam and unknown requests, and investigate denied pushes.

## Verify
- [ ] Prompts denied, password changed, no new prompts afterwards.
- [ ] Source of the password leak identified.

## Checked
Method: 2026-11-08 read the CISA number-matching fact sheet (PDF, read via a saved copy) and the Microsoft Entra number-matching page. Removed as unsupported: Google prompt number behaviour, "services rate-limit prompts", Have I Been Pwned and sign-out-all-sessions steps (kept change-password, marked as judgement), and the claim that passkeys cannot be push-bombed was restated via CISA's phishing-resistant rating.
