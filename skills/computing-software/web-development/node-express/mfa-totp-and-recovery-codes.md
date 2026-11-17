---
id: computing-software.web-development.node-express.mfa-totp-and-recovery-codes
name: mfa-totp-and-recovery-codes
category: computing-software
field: web-development
product: node-express
tags: [authentication-failures, web-authentication, mfa, totp, two-factor-authentication, recovery-codes, otpauth, rfc6238, step-up-authentication]
level: practitioner
status: verified
description: "Adding TOTP two-factor auth: enrolment with QR and confirmation, verification window and replay protection, encrypted secrets, recovery codes and resets."
sources:
  - https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
  - https://www.rfc-editor.org/rfc/rfc6238
  - https://github.com/google/google-authenticator/wiki/Key-Uri-Format
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFA: TOTP and recovery codes

**Goal:** a stolen password alone can't log in, enrolment can't lock users out, and recovery is not the weak link.

## 1. Enrolment
1. Generate a random 160-bit secret (base32); store it **encrypted** (app-level key/KMS), marked unconfirmed.
2. Show QR of `otpauth://totp/Example:alice@example.com?secret=BASE32&issuer=Example&algorithm=SHA1&digits=6&period=30` plus the text secret.
3. Require the user to enter a current code before enabling - catches clock/scan errors.
4. Generate 10 single-use **recovery codes**, show once, store **hashed** (like passwords).
5. Re-authenticate (password) before enrolment changes; notify by email on enable/disable.

## 2. Verification
```js
import { authenticator } from 'otplib';      // otplib 12.x; 13 removed `authenticator` (see below)
authenticator.options = { window: 1 };       // accept previous/next 30 s step for clock drift
const ok = authenticator.check(code, secret);
```
In otplib 13 the equivalent is functional: `import { generateSecret, generateURI, verifySync } from 'otplib'; const r = verifySync({ secret, token: code, epochTolerance: 30, afterTimeStep: user.lastStep }); if (r.valid) user.lastStep = r.timeStep;` (`epochTolerance` is in seconds; `afterTimeStep` rejects replays; both run against 13.5.0). In 12.0.1 `generateSecret(20)` gives 32 base32 characters = 160 bits, and a code from the previous 30 s step is accepted while one from two steps ago is not.
- Store the last used time-step per user and reject reuse (replay within the window); RFC 6238 T=59 with the SHA-1 test secret and 8 digits gives `94287082` in both otplib versions.
- Rate-limit attempts (e.g. 5 per 15 min per account) - 6 digits is only 10^6 possibilities.
- Compare in constant time (libraries do).
- Login flow: password OK -> session marked `mfaPending` (no access) -> code OK -> **regenerate session** -> full access.

## 3. Recovery
- Recovery code consumes one hash; prompt to regenerate when few remain.
- Support-assisted reset is the classic bypass: require strong identity verification, add a delay + notifications.
- Encourage a second factor (passkey) so recovery is rarely needed.

## 4. Factor strength
TOTP is phishable (real-time relay). SMS OTP is weaker still (SIM swap) - allowed as fallback only. Passkeys/WebAuthn are phishing-resistant; offer them as the preferred MFA (see passkeys skill).

## 5. Remember device
Optional signed, long-lived "trusted device" cookie per device, revoked on password change; never skip MFA for new IP + new device.

## Verify
- [ ] Enrolment cannot complete without a valid code; the QR scans in the authenticator apps you support.
- [ ] Same code used twice within 30 s: second attempt rejected.
- [ ] Recovery code works once; the hash list shrinks.
