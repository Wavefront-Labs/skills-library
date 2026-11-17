---
id: computing-software.email-administration.mail-server-administration.greylisting-tradeoffs
name: greylisting-tradeoffs
category: computing-software
field: email-administration
product: mail-server-administration
tags: [greylisting-tradeoffs, greylist-allowlists]
level: practitioner
status: draft
description: "Decide whether greylisting is still worth it today versus Rspamd scoring: delay, retry behaviour and bypass lists."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Greylisting tradeoffs

**Goal:** a reasoned decision, not a default.
## Considerations
- Benefit: removes bots that never retry; cost: first-message delay (minutes to hours).
- Modern spammers often retry; greylisting alone catches less than it used to (unconfirmed, measure in your logs).
- Alternatives: postscreen tests and Rspamd's greylisting module scored only for suspicious mail.
## Steps
1. Measure: count greylisted then passed vs never returned from your logs for a week.
2. Allowlist transactional senders you depend on.
3. Consider enabling greylisting only for messages that already score as suspicious.
## Failure modes
- Users complain about delayed signup mail; add allow rules, do not disable blindly.
## Verify
- Compare spam-folder rate and complaint tickets before and after.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
