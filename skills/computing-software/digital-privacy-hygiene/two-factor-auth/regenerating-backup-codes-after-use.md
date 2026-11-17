---
id: computing-software.digital-privacy-hygiene.two-factor-auth.regenerating-backup-codes-after-use
name: regenerating-backup-codes-after-use
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, backup-code-regeneration, backup-codes, recovery-codes, code-exposure, google-backup-codes, github-recovery-codes]
level: intro
status: draft
description: "Regenerate 2FA backup codes when you've used some, when a copy may have been seen or photographed, or after re-enrolling 2FA, and replace every stored copy."
sources:
  - "https://support.google.com/accounts/answer/1187538"
  - "https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/configuring-two-factor-authentication-recovery-methods"
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Regenerating backup codes

**Goal:** never be down to your last code, and never leave valid codes in a place
you no longer control.

## Triggers
- Used half the codes (Google gives 10; GitHub 16).
- A copy may be exposed: photographed, left in a printer, in a lost bag, emailed,
  or stored on a device you sold.
- Re-enrolled 2FA (some sites keep old codes valid; some invalidate them; don't assume).
- Annual review.

## How (examples)
- **Google**: myaccount.google.com > Security > 2-Step Verification > Backup codes >
  **Get new codes** (old set becomes invalid).
- **GitHub**: Settings > Password and authentication > Recovery codes > **Generate new
  recovery codes**.
- **Microsoft**: Advanced security options > Recovery code > Generate a new code.
- **Bitwarden**: Two-step login > View recovery code (it changes after use).

## Replace every copy
Regeneration invalidates the old set, so update **all** storage locations the same day:
home sheet, off-site copy, vault item. Shred old printouts (cross-cut) once replaced.

## Gotchas
- Regenerating while an old printout is off-site means that copy is now useless until
  you swap it; schedule the visit.
- Some services (banks) issue codes only via support; note which.

## Verify
- [ ] Sign-in test with one new code works (then you have one fewer; that's fine).
- [ ] All stored copies show the same regeneration date.
