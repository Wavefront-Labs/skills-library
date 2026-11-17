---
id: computing-software.collaboration-platform-administration.exchange-online.dmarc-rollout
name: dmarc-rollout
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [dmarc-rollout]
level: advanced
status: draft
description: Move a domain from p=none to enforcement using reports.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DMARC rollout
**Goal:** Move a domain from p=none to enforcement using reports.

- Start: `_dmarc.<d> TXT v=DMARC1; p=none; rua=mailto:<reports mailbox>`.
- Review aggregate reports and fix legitimate senders (SPF/DKIM alignment).
- Then `p=quarantine; pct=25`, increase pct, then `p=reject`.
- Set `sp=` for subdomains.

## Gotchas
- Marketing/ticketing tools often send as your domain without alignment; inventory them first.
- Receivers' reports can be large; use a parsing service.

## Self-check
Reports show >99% aligned pass before moving to the next policy step.
