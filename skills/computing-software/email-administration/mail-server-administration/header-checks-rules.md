---
id: computing-software.email-administration.mail-server-administration.header-checks-rules
name: header-checks-rules
category: computing-software
field: email-administration
product: mail-server-administration
tags: [header-checks-rules, header-body-checks, header-checks, pcre-table, regexp-table]
level: practitioner
status: docs-checked
description: "Write Postfix header_checks with regexp or pcre tables to reject, hold or strip headers, and test them with postmap -q."
sources:
  - https://www.postfix.org/header_checks.5.html
  - https://www.postfix.org/DATABASE_README.html
  - https://www.postfix.org/postmap.1.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Header checks rules

**Goal:** pattern-based message policy (header_checks(5)).
## Steps
1. `header_checks = regexp:/etc/postfix/header_checks`
2. Rules: `/^Subject: .*viagra/i  REJECT` , `/^X-Mailer: Bad/  HOLD`, `/^Received: from .*\[192\.0\.2\.5\]/ IGNORE`.
3. No `postmap` step is needed for regexp tables, but changed regexp:/pcre: files are only re-read after `postfix reload` (DATABASE_README).
## Failure modes
- Expensive regexes slow every message; anchor patterns.
- Rejecting on a word in Subject catches legitimate mail; prefer HOLD while tuning.
- Headers added by milters are not covered by `header_checks`; header_checks(5) lists `milter_header_checks` for that.
## Verify
- `postmap -q "Subject: viagra" regexp:/etc/postfix/header_checks` prints the action.
- Send a matching message in staging and confirm the action (REJECT, HOLD) happens.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): header_checks(5), DATABASE_README, postmap(1).
Confirmed: `header_checks`, `milter_header_checks`, `postmap -q "string" pcre:/file` testing, no index step for regexp/pcre/cidr/texthash tables.
Corrected or removed: the claim that milter-added headers are invisible (rewritten to cite milter_header_checks), the unconfirmed log line.
Method: documentation only; no commands were run.
