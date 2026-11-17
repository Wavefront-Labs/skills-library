---
id: computing-software.email-administration.mail-server-administration.srs-forwarding
name: srs-forwarding
category: computing-software
field: email-administration
product: mail-server-administration
tags: [srs-forwarding, forwarding-srs, srs, sender-rewriting-scheme, postsrsd]
level: advanced
status: draft
description: "Forward mail without breaking SPF by rewriting the envelope sender with SRS (Sender Rewriting Scheme)."
sources:
  - https://www.postfix.org/documentation.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Srs forwarding

**Goal:** forwarded mail still passes SPF at the final receiver.
## Steps
1. Install an SRS daemon (for example postsrsd) and wire it into `sender_canonical_maps` and `recipient_canonical_maps` using the sockets it documents.
2. Rewrite only forwarded mail, not local submissions.
3. Keep the SRS secret out of version control.
## Failure modes
- Bounces to SRS addresses fail if the secret is lost or rotated without grace.
## Verify
- Forward a test message; the final header has `Return-Path` with an `SRS0=` local part and SPF passes.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
