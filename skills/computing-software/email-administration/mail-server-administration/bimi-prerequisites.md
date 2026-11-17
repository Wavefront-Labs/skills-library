---
id: computing-software.email-administration.mail-server-administration.bimi-prerequisites
name: bimi-prerequisites
category: computing-software
field: email-administration
product: mail-server-administration
tags: [bimi-prerequisites, bimi, bimi-record, svg-logo]
level: advanced
status: draft
description: "Check the prerequisites for BIMI: enforced DMARC (quarantine or reject), an SVG logo and, for some mailbox providers, a certificate."
sources:
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bimi prerequisites

**Goal:** know whether your domain can show a brand logo (BIMI is an IETF draft; provider requirements vary, treat details as unconfirmed).
## Steps
1. Enforce DMARC at `p=quarantine` or `p=reject` first (BIMI builds on it).
2. Prepare the logo in the SVG profile BIMI requires (SVG Tiny PS; check the current BIMI Group spec).
3. Publish `default._bimi.example.com. TXT "v=BIMI1; l=https://example.com/logo.svg; a="` (the `a=` evidence certificate is optional for some providers).
4. Confirm each target mailbox provider's current rules; they differ and change.
## Failure modes
- DMARC at p=none: no BIMI display.
- Logo served over plain HTTP or in a non-compliant SVG.
## Verify
- `dig +short TXT default._bimi.example.com`; use the provider's checker where one is available.

## Notes
- Written from the cited documentation; not run end to end here, so confirm option names against your Postfix/Dovecot version.
- Change one thing at a time in staging and keep a copy of the previous config.
