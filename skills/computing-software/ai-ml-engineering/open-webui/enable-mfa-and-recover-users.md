---
id: computing-software.ai-ml-engineering.open-webui.enable-mfa-and-recover-users
name: enable-mfa-and-recover-users
category: computing-software
field: ai-ml-engineering
product: open-webui
tags: [api-keys-mfa, mfa, totp, recovery-codes, authentication, open-webui]
level: practitioner
status: docs-checked
description: "Turn on instance-wide TOTP two-factor sign-in in Open WebUI, understand its requirements and limits, and reset a user who lost their authenticator."
sources:
  - https://docs.openwebui.com/features/authentication-access/mfa
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: require an authenticator code at every sign-in and be able to recover locked-out users.

## Requirements (checked at startup)
`WEBUI_AUTH=True`, `ENABLE_PERSISTENT_CONFIG=True`, and a stable key: secrets are encrypted with a key derived from `WEBUI_SECRET_KEY`, or `MFA_ENCRYPTION_KEY` if set. Changing the key after enrolment makes Open WebUI refuse to start with `ValueError: Stored MFA secrets cannot be decrypted...`; restore the old key.

## Turn on
Settings > Admin > Authentication > Multi-factor authentication > **Require an authenticator for all users**. Optional exemptions: **Allow OAuth sign-in without an authenticator**, **Allow trusted-header sign-in without an authenticator** (use only if the provider/proxy enforces its own second factor). Save. Env equivalents `ENABLE_MFA`, `MFA_ALLOW_OAUTH_BYPASS`, `MFA_ALLOW_TRUSTED_HEADER_BYPASS` set only the starting value; the saved admin-panel value wins afterward. Only an admin sign-in session can change these; API keys are refused.

Warning: saving any change signs every user out of every device, including you.

## User flow
First sign-in: scan the QR (or enter key manually), enter the six-digit code, then save ten one-time recovery codes. Later sign-ins: code, or **Use a recovery code**. Codes are 30 s TOTP with one step of tolerance each side, each used once; the second step must finish within 5 minutes. Users manage it at Settings > Account > Multi-factor authentication (**Replace authenticator**, **Generate recovery codes**); both need a current code and a sign-in within 5 minutes, and sign the account out everywhere.

## Recover a user who lost phone and codes
Verify identity, then on the server:
```bash
open-webui mfa reset user@example.com --reason "Lost phone, identity confirmed"
# Docker image:
docker exec -it open-webui python -c "from open_webui import app; app()" mfa reset user@example.com --reason "..."
```
This removes the authenticator and recovery codes, signs them out everywhere and prints a one-time recovery token valid 30 minutes. The user signs in with password, enters it in **Operator recovery token**, then re-enrols. `--reason` is required; the command needs the same database and `WEBUI_SECRET_KEY` (env or `.webui_secret_key` file in the current directory).

## Rate limits while MFA is on
10 password/LDAP attempts per account per 15 min; 10 code attempts per account per 15 min; 5 codes per sign-in; 100 mutating requests per IP per 15 min on `/api/v1/auths` (Redis-shared if configured). Set `FORWARDED_ALLOW_IPS` to your proxy so real client IPs are used.

## Gotchas
- API keys still work without a code; use them for automation. API sign-in and OAuth token exchange return an MFA step instead of a token unless exempted.
- Pending accounts get no session while MFA is on; the custom pending overlay (`PENDING_USER_OVERLAY_TITLE`/`_CONTENT`) only shows with MFA off.
- Events for Event functions and audit log: `auth.mfa.enrolled`, `.replaced`, `.failed`, `.recovery_used`, `.recovery_codes_regenerated`, `.policy_changed`.

## Checked
2026-11-04. Confirmed against the Open WebUI docs page features/authentication-access/mfa (read in full): startup requirements and the exact ValueError text, the admin switches and two exemptions, the three env variables and their first-start-only effect, admin-session-only changes, sign-out on save, first-time enrolment with ten recovery codes, 30 second codes with one-step tolerance and the five-minute window, the account management actions, the mfa reset command in both forms with the 30 minute token and required reason, the four attempt limits and FORWARDED_ALLOW_IPS, API key and token exchange behaviour, the pending overlay note and the six event names. Nothing removed.
Method: documentation only; no commands were run.
