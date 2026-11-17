---
id: computing-software.collaboration-platform-administration.exchange-online.transport-rules
name: transport-rules
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [transport-rules, exo-mail-flow-rules]
level: practitioner
status: draft
description: Build mail flow rules with conditions, actions and exceptions, testing before enforce.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Mail flow (transport) rules
**Goal:** Build mail flow rules with conditions, actions and exceptions, testing before enforce.

- Exchange admin center > Mail flow > Rules, or `New-TransportRule -Name 'Tag external' -FromScope NotInOrganization -PrependSubject '[EXTERNAL] ' -Mode Audit`.
- Modes: Enforce, Test with Policy Tips, Test without Policy Tips (Audit).
- Order matters; use priority and `StopRuleProcessing` carefully.
- Common cases: disclaimers, external tagging, blocking attachment types, redirecting to quarantine.

## Gotchas
- Rules apply on transit, not to messages already delivered.
- Replacing the anti-spam bypass with a rule 'set SCL -1' lowers protection; document it.

## Self-check
Send a test message and check Message trace for the rule hit.
