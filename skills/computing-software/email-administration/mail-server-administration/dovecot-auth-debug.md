---
id: computing-software.email-administration.mail-server-administration.dovecot-auth-debug
name: dovecot-auth-debug
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dovecot-auth-debug, auth-debug, doveadm-auth-test, login-failure]
level: practitioner
status: docs-checked
description: "Troubleshoot Dovecot logins with auth_debug, doveadm auth test and doveadm user."
sources:
  - https://doc.dovecot.org/2.3/admin_manual/debugging/debugging_authentication/
  - https://doc.dovecot.org/2.3/settings/core/
  - https://doc.dovecot.org/main/core/man/doveadm-auth.1/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dovecot auth debug

**Goal:** find why a login fails.
## Steps
1. `doveadm auth test user@example.com` (prompts for the password) tests the passdb lookup.
2. `doveadm user -u user@example.com` shows the userdb result; `doveadm auth login user@example.com password` simulates a full login with both lookups.
3. Temporarily set `auth_debug = yes` (it also enables `auth_verbose`; passwords are logged as `<hidden>`), reload, read the log, then turn it off. `auth_debug_passwords = yes` logs passwords and the scheme on mismatch; avoid it.
4. In Dovecot 2.4 `auth_debug` is replaced by the `log_debug` filter, for example `log_debug=category=auth`.
## Failure modes
- Debug left on in production fills logs and may expose sensitive data.
- Mismatch between SASL username (with domain) and passdb key.
## Verify
- `doveadm auth test` prints `passdb: <user> auth succeeded` (man page example); after the fix, the mail client logs in.

## Notes
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked

2026-11-03. Confirmed in the Dovecot 2.3 docs (Debugging Authentication, settings auth_debug and auth_debug_passwords), the doveadm-auth man page (password prompt, success output) and the 2.3 to 2.4 converted-settings table (auth_debug replaced by log_debug). Removed an unsourced log line pattern.

Method: documentation only; no commands were run.
