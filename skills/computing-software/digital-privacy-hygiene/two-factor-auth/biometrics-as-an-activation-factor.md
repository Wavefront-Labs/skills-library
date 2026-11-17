---
id: computing-software.digital-privacy-hygiene.two-factor-auth.biometrics-as-an-activation-factor
name: biometrics-as-an-activation-factor
category: computing-software
field: digital-privacy-hygiene
product: two-factor-auth
tags: [digital-privacy-hygiene, two-factor-auth, biometric-activation-factor, biometric-unlock, syncable-authenticators]
level: practitioner
status: draft
description: "Understand why fingerprint and face unlock only activate a device-held key rather than authenticate you remotely, and where that breaks down."
sources:
  - "https://pages.nist.gov/800-63-4/sp800-63b.html"
  - "https://support.apple.com/guide/security/face-id-and-touch-id-security-sec067eb0c9e/web"
  - "https://source.android.com/docs/security/features/biometric"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Biometrics as an activation factor

**Goal:** know what Face ID, Touch ID, Windows Hello and fingerprint sensors actually protect, so you rely on them
correctly.

## How it works
- The biometric match happens **locally** in a secure element/TPM/TEE. A successful match releases a key that
  signs the challenge (passkey) or unlocks the vault.
- The website never sees your fingerprint; it sees a signature from the device key. So the factors are
  "something you have" (device) activated by "something you are".
- NIST SP 800-63B-4 allows biometrics only as part of MFA with a physical authenticator, requires presentation
  attack detection, and limits consecutive failures before requiring another activation method.

## Implications
| Situation | Effect |
|---|---|
| Someone forces your finger/face | Biometric unlocks the device; switch to passcode-only in high-risk moments |
| Passcode known to an attacker | They can enrol their own biometric or bypass it; the passcode is the real secret |
| Twins/children for Face ID | Higher false-match rate; prefer passcode for kids' access |
| Biometric data "leak" | Templates stay on device; not used by sites |

## Quick lockout
- iPhone: press side + volume buttons until the slider shows; Face ID disabled until passcode.
- Android: Power menu > **Lockdown**.
- Windows: Win+L then require PIN; or disable Hello biometrics in high-risk travel.

## Gotchas
- Biometric fallback is always the passcode/PIN; make it strong.
- Re-enrolled fingerprints on Android don't invalidate keys in all apps; check app settings (some invalidate
  on new enrolment, which is a feature).
