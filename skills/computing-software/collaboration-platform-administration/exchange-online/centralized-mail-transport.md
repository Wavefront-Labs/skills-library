---
id: computing-software.collaboration-platform-administration.exchange-online.centralized-mail-transport
name: centralized-mail-transport
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [centralized-mail-transport]
level: advanced
status: draft
description: Route outbound internet mail via on-premises for compliance appliances.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Centralized mail transport
**Goal:** Route outbound internet mail via on-premises for compliance appliances.

- HCW option 'Centralized Mail Transport' routes cloud mail out through on-premises send connector.
- Cloud outbound connector uses smart host and TLS.
- Impact: hybrid servers must be sized for all mail.
- Disable when the on-prem appliance retires.

## Gotchas
- Creates a single point of failure on premises.
- Mail loops if connectors and accepted domains disagree.

## Self-check
Message trace shows hops via the on-premises connector.
