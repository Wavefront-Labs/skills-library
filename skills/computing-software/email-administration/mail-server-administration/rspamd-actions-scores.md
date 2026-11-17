---
id: computing-software.email-administration.mail-server-administration.rspamd-actions-scores
name: rspamd-actions-scores
category: computing-software
field: email-administration
product: mail-server-administration
tags: [rspamd-actions-scores, rspamd-actions, rspamd-scores, metric-actions]
level: advanced
status: draft
description: "Set Rspamd actions (greylist, add header, rewrite subject, reject) and tune symbol scores via local.d."
sources:
  - https://rspamd.com/doc/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Rspamd actions scores

**Goal:** map scores to outcomes.
## Steps
1. `local.d/actions.conf`: `reject = 15; add_header = 6; greylist = 4;` (example values; start from the shipped defaults).
2. Adjust a symbol in `local.d/groups.conf` or via the web UI.
3. Use `rspamc symbols < msg.eml` to see symbol hits.
## Failure modes
- Lowering reject too aggressively; start with add_header only and review.
- Greylist action conflicts with Postfix greylisting: pick one layer.
## Verify
- Run known ham/spam samples through `rspamc` and compare result and action.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
