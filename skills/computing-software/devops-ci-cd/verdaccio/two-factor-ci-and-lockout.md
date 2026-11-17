---
id: computing-software.devops-ci-cd.verdaccio.two-factor-ci-and-lockout
name: two-factor-ci-and-lockout
category: computing-software
field: devops-ci-cd
product: verdaccio
tags: [two-factor, totp, otp, otp-ci, lockout, secret-rotation, bypass-2fa]
level: advanced
status: docs-checked
description: "Run two-factor safely: CI options without bypass tokens, five-failure lockout, secret rotation locking users out, and fixes for EOTP, 503 and rejected codes."
sources:
  - https://verdaccio.org/docs/two-factor-authentication/
  - https://verdaccio.org/docs/staged-publishing/
  - https://verdaccio.org/docs/setup-npm/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
CI problem: with auth-and-writes a pipeline cannot produce a one-time code (codes are single use, about 90 seconds). Options:
- publish from an account in auth-only mode (or no 2FA) protected by package access rules;
- use staged publishing: CI runs `npm stage publish` (no code) and a person approves with a code.
Verdaccio does not implement npmjs-style `bypass_2fa` automation tokens.

Lockout: after five wrong codes, OTPs are refused for five minutes, even correct ones. Reads and installs keep working.

Secret rotation: 2FA records are encrypted with the server secret (`config.secret` or `VERDACCIO_LEGACY_ENCRYPTION_KEY`). Rotating it makes every record undecryptable (log: `the two-factor record of alice could not be decrypted`). No self-service recovery: ask users to disable 2FA first, re-enable after. A user locked out with no recovery codes needs an operator to remove their record from the storage backend.

Troubleshooting:
- `EOTP` in a script: pass `--otp=<code>`.
- Codes always rejected: clock drift; check NTP (window is one 30-second step either side).
- `503 the two-factor authentication is not yet supported`: flag off or no restart.
- Plain `401 need: Bearer`: server lacks 2FA support.

Limits: TOTP only, no WebAuthn, CLI-only enrolment, no web login flow.

## Checked

2026-11-04. Read the Verdaccio documentation pages: Two-factor authentication, Staged publishing and Setup npm. Confirmed: the CI options, no bypass_2fa, the five-failure five-minute lockout, secret rotation and the log message, the EOTP, 503 and Bearer troubleshooting, the 30-second step either side, the limits, and the ninety-second code life from the npm page. Removed or corrected: nothing.

Method: documentation only; no commands were run.
