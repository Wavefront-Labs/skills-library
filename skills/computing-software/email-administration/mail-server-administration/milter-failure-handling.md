---
id: computing-software.email-administration.mail-server-administration.milter-failure-handling
name: milter-failure-handling
category: computing-software
field: email-administration
product: mail-server-administration
tags: [milter-failure-handling, milter-default-action, milter-timeouts]
level: advanced
status: docs-checked
description: "Choose milter_default_action and timeouts so a crashed milter neither loses mail nor blindly accepts spam."
sources:
  - https://www.postfix.org/MILTER_README.html
  - https://www.postfix.org/postconf.5.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Milter failure handling

**Goal:** predictable behaviour when a filter is down.
## Steps
1. `milter_default_action`: `tempfail` rejects further commands with a temporary status (senders retry); `accept` proceeds as if the filter were absent; `reject` is permanent; `shutdown` (Postfix 3.11+, the 3.11 default; earlier default `tempfail`) closes the SMTP connection with a 421 for smtpd_milters.
2. Tune `milter_connect_timeout` (30s), `milter_command_timeout` (30s), `milter_content_timeout` (300s).
3. Monitor the milter service and alert on Postfix milter errors in the mail log.
## Failure modes
- tempfail during a long filter outage fills the sender queues and may bounce after their retry limit.
- accept during an outage lets spam and unsigned mail through silently.
## Verify
- Stop the milter in staging; confirm mail is temporarily rejected with tempfail, and delivered with accept.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.

## Checked
Date: 2026-11-02. Documentation: Postfix source docs (vdukhovni/postfix html/ tree, same text as postfix.org): postconf(5), MILTER_README.
Confirmed: `milter_default_action` values and defaults, `milter_connect_timeout`, `milter_command_timeout`, `milter_content_timeout` defaults.
Corrected or removed: the exact 451 4.7.1 text and the `milter ... unreachable` log string.
Method: documentation only; no commands were run.
