---
id: computing-software.email-administration.mail-server-administration.envelope-vs-header-from
name: envelope-vs-header-from
category: computing-software
field: email-administration
product: mail-server-administration
tags: [envelope-vs-header-from, message-format, envelope-sender, return-path, header-from]
level: practitioner
status: docs-checked
description: "Tell the SMTP envelope (MAIL FROM, RCPT TO) apart from header From/To, and why SPF, DKIM and DMARC look at different ones."
sources:
  - https://www.rfc-editor.org/rfc/rfc5322
  - https://www.rfc-editor.org/rfc/rfc5321
  - https://www.rfc-editor.org/rfc/rfc7208
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Envelope vs header from

**Goal:** know which identity each authentication check uses.
## Facts
- The envelope sender is the MAIL FROM (reverse-path) of the SMTP transaction (RFC 5321). A server making final delivery inserts a `Return-Path:` line carrying that address.
- SPF checks the MAIL FROM identity and also the HELO identity (RFC 7208). With a null MAIL FROM, as in many bounces, only the HELO identity is available.
- The header `From:` (RFC 5322) is the author address and is what DMARC aligns against: SPF and DKIM must pass and be in alignment with the RFC5322.From domain (RFC 7489).
- DKIM authenticates the domain in the `d=` tag of the signature; DMARC then compares it with the RFC5322.From domain.
- A `Bcc:` field may be removed from the copies sent to other recipients (RFC 5322), so blind recipients are known to the envelope, not to the visible headers.
## Steps
1. Look at a delivered message and compare `Return-Path:` with `From:`.
2. Compare them with the authentication results your receiving system recorded for each identity.
## Failure modes
- Mailing lists commonly rewrite the MAIL FROM identity, which affects SPF results (RFC 7208 notes almost all lists do).
- A spoofed From can still pass SPF for the sender's own envelope domain; only DMARC alignment ties the result to the From domain.
## Verify
- Send a test to a mailbox you control and map each header to its check.

## Checked

2026-11-09. Confirmed on RFC 5321 (return-path line inserted at final delivery), RFC 7208 (MAIL FROM and HELO identities, null MAIL FROM, mailing lists rewriting MAIL FROM), RFC 7489 (alignment with RFC5322.From, DKIM d= domain), and RFC 5322 (Bcc handling). Removed: the Authentication-Results examples (not in these RFCs) and the boilerplate notes.

Method: documentation only; no commands were run.
