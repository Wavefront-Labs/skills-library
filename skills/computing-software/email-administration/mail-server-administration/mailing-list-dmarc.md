---
id: computing-software.email-administration.mail-server-administration.mailing-list-dmarc
name: mailing-list-dmarc
category: computing-software
field: email-administration
product: mail-server-administration
tags: [mailing-list-dmarc, from-rewriting, list-munging]
level: advanced
status: draft
description: "Handle mailing lists under DMARC: From rewriting, Reply-To, subject tags and keeping DKIM valid."
sources:
  - https://www.rfc-editor.org/rfc/rfc8617
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mailing list dmarc

**Goal:** keep list mail deliverable when subscribers' domains publish p=reject.
## Steps
1. Prefer not to modify subject/body so original DKIM survives.
2. Otherwise rewrite From to a list address (for example `"Alice via List" <list@example.org>`) and set Reply-To to the author.
3. Re-sign with the list domain's DKIM and add ARC if possible.
## Failure modes
- Subject tags and footers invalidate the author's DKIM, leading to DMARC reject.
## Verify
- Send a test from a p=reject domain through the list; recipients receive it with `dmarc=pass`.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
