---
id: computing-software.collaboration-platform-administration.exchange-online.dkim-signing
name: dkim-signing
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [dkim-signing]
level: practitioner
status: draft
description: Enable DKIM for custom domains with the two selector CNAMEs.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# DKIM signing in Exchange Online
**Goal:** Enable DKIM for custom domains with the two selector CNAMEs.

- Publish CNAMEs `selector1._domainkey.<d>` and `selector2._domainkey.<d>` to the targets from `Get-DkimSigningConfig -Identity <d>`.
- `Set-DkimSigningConfig -Identity <d> -Enabled $true`.
- Defender portal > Email & collaboration > Policies > Email authentication settings > DKIM.
- Rotate with `Rotate-DkimSigningConfig -KeySize 2048`.

## Gotchas
- Enabling before the CNAMEs resolve fails.
- Third-party senders need their own DKIM aligned to your domain.

## Self-check
A sent message's headers show dkim=pass header.d=<your domain>.
