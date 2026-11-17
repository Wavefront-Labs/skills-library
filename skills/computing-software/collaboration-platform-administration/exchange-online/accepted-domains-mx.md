---
id: computing-software.collaboration-platform-administration.exchange-online.accepted-domains-mx
name: accepted-domains-mx
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [accepted-domains-mx]
level: practitioner
status: draft
description: Choose authoritative vs internal relay domains and align MX.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Accepted domains and MX routing
**Goal:** Choose authoritative vs internal relay domains and align MX.

- `Get-AcceptedDomain`; `Set-AcceptedDomain -Identity <d> -DomainType InternalRelay` for coexistence.
- MX points to the EOP host; SPF includes spf.protection.outlook.com.
- With a third-party gateway first, lock down inbound to gateway IPs via connector.
- Remove the old MX only after the new one propagates.

## Gotchas
- Authoritative domain rejects mail for non-existent recipients; relay domain forwards it.
- Lower TTL before MX change for faster rollback.

## Self-check
`nslookup -type=MX <domain>` returns the intended host.
