---
id: computing-software.email-administration.mail-server-administration.spamassassin-tuning
name: spamassassin-tuning
category: computing-software
field: email-administration
product: mail-server-administration
tags: [spamassassin-tuning, spamassassin, local-cf, sa-update, required-score]
level: practitioner
status: draft
description: "Tune SpamAssassin: required_score, local.cf scores, custom rules and updating rules with sa-update."
sources:
  - https://spamassassin.apache.org/doc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Spamassassin tuning

**Goal:** score spam with rules you control.
## Steps
1. `/etc/spamassassin/local.cf`: `required_score 5.0`, `score MY_RULE 2.0`, `header MY_RULE Subject =~ /campaign/i`.
2. Update rules: `sa-update`, then restart `spamd`.
3. Debug a message: `spamassassin -D < msg.eml 2>&1 | less`, or `spamc -R < msg.eml`.
4. Lint: `spamassassin --lint`.
## Failure modes
- Large custom scores for common words cause false positives.
- No `sa-update` schedule: rules age.
## Verify
- `spamassassin --lint` prints nothing; test messages show the `X-Spam-Status` header with rule hits.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
