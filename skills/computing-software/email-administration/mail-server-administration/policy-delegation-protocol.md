---
id: computing-software.email-administration.mail-server-administration.policy-delegation-protocol
name: policy-delegation-protocol
category: computing-software
field: email-administration
product: mail-server-administration
tags: [policy-delegation-protocol, postfix-policy, check-policy-service, policy-daemon, smtpd-policy]
level: advanced
status: docs-checked
description: "Plug an external policy daemon into smtpd with check_policy_service and understand its request/response protocol."
sources:
  - https://www.postfix.org/SMTPD_POLICY_README.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy delegation protocol

**Goal:** let an external process decide on each RCPT (SMTPD_POLICY_README).
## Steps
1. `smtpd_recipient_restrictions = ..., reject_unauth_destination, check_policy_service unix:private/policy`.
2. Postfix sends name=value lines (request, client_address, sender, recipient, ...) ending with a blank line.
3. The server replies with one `action=...` attribute (for example `action=DUNNO`, `action=DEFER_IF_PERMIT text`, `action=REJECT text`) followed by an empty line.
4. `smtpd_policy_service_timeout` (default 100s); to fail open on an unavailable service, use the documented per-service `timeout`/`default_action` override (SMTPD_POLICY_README shows `default_action=DUNNO`).
## Failure modes
- Hung policy daemon stalls SMTP until the timeout; monitor the daemon.
- Put it after `reject_unauth_destination` so you do not run it for relay attempts.
## Verify
- Stop the daemon in staging and confirm the result matches your intended default action.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): SMTPD_POLICY_README, postconf(5).
Confirmed: `check_policy_service`, `request=smtpd_access_policy` name=value requests terminated by an empty line, one `action=` reply plus empty line, `DUNNO` and `DEFER_IF_PERMIT`, `smtpd_policy_service_timeout` default 100s, per-service `default_action=DUNNO` example.
Corrected or removed: the claim that Postfix defers on timeout (the README configures default_action), the log-string verification.
Method: documentation only; no commands were run.
