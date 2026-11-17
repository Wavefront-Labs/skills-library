---
id: computing-software.collaboration-platform-administration.exchange-online.anti-spam-phish-policies
name: anti-spam-phish-policies
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [anti-spam-phish-policies, exo-eop-mdo-protection]
level: practitioner
status: draft
description: Tune threat policies via preset policies first, then custom.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Anti-spam, anti-malware and anti-phishing policies
**Goal:** Tune threat policies via preset policies first, then custom.

- Defender portal > Email & collaboration > Policies & rules > Threat policies.
- Apply Standard or Strict preset security policies to users, then custom policies for exceptions.
- Anti-phishing impersonation: add protected users and domains.
- Anti-malware: common attachment filter; zero-hour auto purge handled by service.

## Gotchas
- Preset policies take precedence over custom; understand priority.
- Allow entries bypass filtering; use Tenant Allow/Block List with expiry.

## Self-check
Test with the Configuration analyzer for deviations from recommended.
