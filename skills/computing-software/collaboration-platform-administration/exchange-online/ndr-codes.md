---
id: computing-software.collaboration-platform-administration.exchange-online.ndr-codes
name: ndr-codes
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [ndr-codes]
level: practitioner
status: draft
description: Decode common non-delivery reports.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# NDR and SMTP status codes
**Goal:** Decode common non-delivery reports.

- Enhanced codes: 5.1.1 bad address, 5.7.1 permission/relay denied, 5.4.1 recipient not found in directory (Directory Based Edge Blocking).
- 4.x.x are temporary; retried.
- 5.7.509 means DMARC reject by sender policy; 5.7.708 relates to traffic blocked for IP reputation (confirm per docs).
- Use Remote Connectivity Analyzer (testconnectivity.microsoft.com) for connectivity.

## Gotchas
- Look up the exact code in Microsoft's NDR documentation before acting.
- Stale autocomplete cache (nickname) is a frequent 5.1.1 cause.

## Self-check
After the fix, a test message gets delivered with status Delivered.
