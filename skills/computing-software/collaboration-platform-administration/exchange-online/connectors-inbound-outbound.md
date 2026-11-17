---
id: computing-software.collaboration-platform-administration.exchange-online.connectors-inbound-outbound
name: connectors-inbound-outbound
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [connectors-inbound-outbound]
level: advanced
status: draft
description: Configure connectors for partners, third-party filtering or on-premises mail.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inbound and outbound connectors
**Goal:** Configure connectors for partners, third-party filtering or on-premises mail.

- Mail flow > Connectors > Add; Partner organization or Your organization's email server.
- Prefer certificate-based identification (CBC) or specific sender IPs for inbound; avoid open IP ranges.
- Outbound: smart host or routing via a defined domain; enable TLS validation.
- Enhanced Filtering for Connectors when a third-party gateway fronts EOP so SPF/IP checks use the original IP.

## Gotchas
- A broad inbound connector with permissive IPs can let spoofing bypass checks.
- Test connector validation in the wizard before saving.

## Self-check
Run the connector validation and a message trace on a test message.
