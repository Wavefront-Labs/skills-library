---
id: computing-software.email-administration.mail-server-administration.spf-policyd-check
name: spf-policyd-check
category: computing-software
field: email-administration
product: mail-server-administration
tags: [spf-policyd-check, policyd-spf, spf-check-inbound]
level: advanced
status: draft
description: "Check inbound SPF in Postfix with postfix-policyd-spf-python or Rspamd and decide reject versus score."
sources:
  - https://www.rfc-editor.org/rfc/rfc7208
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spf policyd check

**Goal:** evaluate SPF for incoming mail and record the result.
## Steps
1. Install a policy daemon, add to master.cf as a spawn service, then `check_policy_service unix:private/policyd-spf` after `reject_unauth_destination`.
2. Set the `policyd-spf.conf` HELO and Mail_From reject mode (for example `Fail` to reject, `False` to only add headers); defaults vary by package.
3. Or let Rspamd's SPF module score it and avoid hard rejects (preferred for forwarding-heavy mail).
## Failure modes
- Hard-rejecting on SPF fail breaks forwarded mail; use DMARC policy to decide.
## Verify
- The `Received-SPF:` or `Authentication-Results` header on a test message shows the result.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
