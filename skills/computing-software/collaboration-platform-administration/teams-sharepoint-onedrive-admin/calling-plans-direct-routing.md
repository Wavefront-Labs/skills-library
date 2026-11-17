---
id: computing-software.collaboration-platform-administration.teams-sharepoint-onedrive-admin.calling-plans-direct-routing
name: calling-plans-direct-routing
category: computing-software
field: collaboration-platform-administration
product: teams-sharepoint-onedrive-admin
tags: [calling-plans-direct-routing, tso-teams-voice]
level: advanced
status: draft
description: Choose Microsoft Calling Plans or connect an SBC with Direct Routing.
sources: ['https://learn.microsoft.com/en-us/microsoftteams/', 'https://learn.microsoft.com/en-us/sharepoint/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-700']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calling Plans and Direct Routing
**Goal:** Choose Microsoft Calling Plans or connect an SBC with Direct Routing.

- Calling Plans: acquire numbers (Voice > Phone numbers), assign to users and emergency address.
- Direct Routing: `New-CsOnlinePSTNGateway -Fqdn sbc.contoso.com -SipSignalingPort 5061 -Enabled $true`, voice routes, PSTN usage and online voice routing policy.
- User needs a Teams Phone licence and `Set-CsPhoneNumberAssignment -Identity <upn> -PhoneNumber +1... -PhoneNumberType DirectRouting`.
- SBC needs a public certificate with a matching domain in the tenant.

## Gotchas
- The SBC FQDN domain must be registered in the tenant with a licensed user.
- Calling Plan availability varies by country.

## Self-check
A test call in and out succeeds; `Get-CsOnlinePSTNGateway` shows the gateway.
