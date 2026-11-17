---
id: computing-software.email-administration.mail-server-administration.body-checks-caution
name: body-checks-caution
category: computing-software
field: email-administration
product: mail-server-administration
tags: [body-checks-caution, body-checks, body-checks-size-limit]
level: advanced
status: docs-checked
description: "Use body_checks sparingly: limits on lines examined, MIME handling, and why heavy content filtering belongs in a milter."
sources:
  - https://www.postfix.org/header_checks.5.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Body checks caution

**Goal:** know the limits of Postfix body_checks.
## Facts
- `body_checks` run per body line, not on decoded attachments; `body_checks_size_limit` caps how much text of each body segment or attachment is inspected (default 51200).
- Encoded content is not decoded for you, so base64 or similar text will not match plain patterns.
## Steps
1. Use `body_checks` only for a few exact strings (for example a known campaign URL).
2. For real content analysis use Rspamd or SpamAssassin through a milter.
3. Use `HOLD` first, review, then switch to `REJECT`.
## Failure modes
- Rejecting legitimate quoted text that matches the pattern.
## Verify
- `postmap -q "buy now" regexp:/etc/postfix/body_checks` returns the rule action if a rule matches (postmap -q "string" works for pcre/regexp tables, per header_checks(5)).

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5) body_checks_size_limit, header_checks(5).
Confirmed: `body_checks`, `body_checks_size_limit` default 51200, `postmap -q` against a pattern table.
Corrected or removed: the default 50000 (real default 51200); the 'cannot parse MIME structure' claim.
Method: documentation only; no commands were run.
