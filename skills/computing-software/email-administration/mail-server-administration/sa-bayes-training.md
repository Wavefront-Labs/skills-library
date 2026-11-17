---
id: computing-software.email-administration.mail-server-administration.sa-bayes-training
name: sa-bayes-training
category: computing-software
field: email-administration
product: mail-server-administration
tags: [sa-bayes-training, sa-learn, bayes, bayes-training]
level: practitioner
status: draft
description: "Train SpamAssassin's Bayes filter with sa-learn from spam and ham corpora and manage its database."
sources:
  - https://spamassassin.apache.org/doc.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sa bayes training

**Goal:** per-site learning.
## Steps
1. Train: `sa-learn --spam /path/to/spam-dir`, `sa-learn --ham /path/to/ham-dir`.
2. Check: `sa-learn --dump magic` shows the token counts.
3. Auto-training thresholds exist but manual feeding from user reports is better.
4. Minimum samples (200 spam and 200 ham in the docs) before Bayes activates.
## Failure modes
- Training on unreviewed spam folders teaches wrong ham.
- Shared database permission mismatch between spamd and the learner.
## Verify
- `BAYES_xx` tests appear in subsequent message headers.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
