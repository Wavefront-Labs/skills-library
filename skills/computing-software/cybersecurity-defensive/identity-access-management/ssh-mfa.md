---
id: computing-software.cybersecurity-defensive.identity-access-management.ssh-mfa
name: ssh-mfa
category: computing-software
field: cybersecurity-defensive
product: identity-access-management
tags: [ssh-mfa, pam-google-authenticator, fido2-ssh-keys, ed25519-sk, authenticationmethods, duo-unix, server-mfa]
level: practitioner
status: docs-checked
description: "Add MFA to SSH logins: FIDO2-backed sk keys with verify-required, AuthenticationMethods with PAM TOTP or Duo, SSH user CA certificates, and handling automation accounts."
sources: ["https://man.openbsd.org/sshd_config", "https://man.openbsd.org/ssh-keygen", "https://github.com/google/google-authenticator-libpam", "https://duo.com/docs/duounix"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# MFA for SSH and servers

## Option 1: FIDO2 security key SSH keys
```
ssh-keygen -t ed25519-sk -O resident -O verify-required
```
- `ed25519-sk` and `ecdsa-sk` are the FIDO key types. `-O verify-required` makes signatures from this key attest that the user was verified (PIN or on-token biometrics); `-O resident` stores a resident key on the authenticator.
- Server side: `PubkeyAuthOptions verify-required` in `sshd_config` requires the FIDO signature to attest user verification. `touch-required` always requires a touch. Neither option affects non-FIDO keys.

## Option 2: key + TOTP via PAM
```
# sshd_config
KbdInteractiveAuthentication yes
UsePAM yes
AuthenticationMethods publickey,keyboard-interactive
# /etc/pam.d/sshd
auth required pam_google_authenticator.so nullok   # nullok lets users without a secret in; drop it after enrolment
```
- `AuthenticationMethods` takes comma-separated methods that must all succeed (here public key, then keyboard-interactive).
- Duo Unix provides a `pam_duo` PAM module as the managed alternative; follow Duo's documentation for configuration.

## Option 3: short-lived SSH certificates
Servers trust a user CA with `TrustedUserCAKeys`; users present certificates signed by it instead of per-user authorized_keys entries. How the certificate is issued (and the MFA step before issuance) depends on your IdP or CA product; consult its documentation.

## Automation
Use a `Match` block in `sshd_config` for service accounts (for example with a narrower `AuthenticationMethods`), and `ForceCommand` to pin the command they may run.

## Gotchas
- Keep a second session open while changing sshd or PAM configuration, so you are not locked out.
- A password in the authentication chain is only as strong as the password; prefer TOTP or FIDO.

## Verify
- [ ] SSH with a key only (no second factor) is rejected for human accounts.
- [ ] Automation accounts are restricted in their `Match` block.

## Checked
2026-11-01. Confirmed against the OpenBSD sshd_config and ssh-keygen manual pages (FIDO key types, resident, verify-required, PubkeyAuthOptions, AuthenticationMethods, TrustedUserCAKeys, Match, ForceCommand), the google-authenticator-libpam README (`pam_google_authenticator`, `nullok`) and Duo Unix docs (`pam_duo`). Removed: OpenSSH version gate, named certificate vendors and cloud services, `from=` and `Match Address` details, `sshd -t`, the `@include common-auth` instruction, `login_duo` and Duo push claims.
Method: documentation only; no commands were run.
