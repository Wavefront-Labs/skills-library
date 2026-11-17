---
id: computing-software.email-administration.mail-server-administration.dmarc-alignment-debug
name: dmarc-alignment-debug
category: computing-software
field: email-administration
product: mail-server-administration
tags: [dmarc-alignment-debug, dmarc-alignment, aspf, adkim, relaxed-alignment]
level: advanced
status: docs-checked
description: "Debug DMARC failures: strict versus relaxed alignment (aspf, adkim), subdomains, forwarding and third-party senders."
sources:
  - https://www.rfc-editor.org/rfc/rfc7489
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Dmarc alignment debug

**Goal:** find why an authenticated message still fails DMARC.
## Steps
1. From the message headers collect: the RFC5322.From domain, the SPF-authenticated domain (smtp.mailfrom), and the DKIM `d=` domain of each validated signature.
2. A message satisfies DMARC if at least one of SPF or DKIM produces a pass and is in alignment with the RFC5322.From domain.
3. Relaxed alignment (the default for both `aspf` and `adkim`, value `r`) requires the Organizational Domains to be equal; strict (`aspf=s`, `adkim=s`) requires an exact match of the fully qualified domain names.
4. Check that a vendor signs with your domain (custom DKIM) rather than its own: a valid signature from another domain does not align.
5. Forwarders and mailing lists can break authentication; aggregate reports mark such mail with the override reasons `forwarded` and `trusted_forwarder`.
## Failure modes
- Vendor signs with its own `d=`: DKIM passes but is not aligned.
- With relaxed mode, `d=example.com` aligns with a From of `alerts@news.example.com`; with strict mode the same pair fails.
- A `d=` of a public suffix such as `com` never aligns.
## Verify
- Send a test message and confirm the receiving system reports a DMARC pass for the From domain.

## Checked

2026-11-09. Confirmed on RFC 7489: section 3.1 alignment definitions and the news.example.com example for relaxed versus strict, the d=com note, the adkim and aspf tags with default r, the at-least-one-of rule for passing DMARC checks, and the forwarded and trusted_forwarder reasons. Removed: the claim that SPF breaks on forwarding as a fixed rule (the RFC only says forwarders can break authentication), the Authentication-Results line, and the boilerplate Postfix/Dovecot notes.

Method: documentation only; no commands were run.
