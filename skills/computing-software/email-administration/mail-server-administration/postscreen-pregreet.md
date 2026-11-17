---
id: computing-software.email-administration.mail-server-administration.postscreen-pregreet
name: postscreen-pregreet
category: computing-software
field: email-administration
product: mail-server-administration
tags: [postscreen-pregreet, deep-protocol-tests, postscreen-greet-wait]
level: advanced
status: draft
description: "Use postscreen pregreet and deep protocol tests to catch bots that talk before the banner, and know the first-contact delay."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Postscreen pregreet

**Goal:** catch clients that speak before the 220 greeting.
## Steps
1. `postscreen_greet_wait = 6s` (shipped default is a few seconds; check `postconf -d`).
2. `postscreen_greet_action = enforce` rejects violators with a 550 once the pregreet test fails.
3. Optionally enable `postscreen_non_smtp_command_enable` and `postscreen_pipelining_enable` (deep tests, off by default).
4. First-time legitimate clients are temporarily rejected once, then cached by `postscreen_cache_retention_time`.
## Failure modes
- Legit senders that retry badly may lose the first message.
- Deep tests add latency and false positives; enable one at a time.
## Verify
- Run `nc` and send text before the banner; confirm `PREGREET` in the log.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
