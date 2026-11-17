---
id: computing-software.collaboration-platform-administration.exchange-online.calendar-sharing-orgs
name: calendar-sharing-orgs
category: computing-software
field: collaboration-platform-administration
product: exchange-online
tags: [calendar-sharing-orgs, exo-calendar-limits]
level: practitioner
status: draft
description: Control internal and external free/busy and calendar detail.
sources: ['https://learn.microsoft.com/en-us/exchange/exchange-online', 'https://learn.microsoft.com/en-us/powershell/exchange/exchange-online-powershell']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calendar sharing and organization relationships
**Goal:** Control internal and external free/busy and calendar detail.

- `Set-MailboxFolderPermission -Identity user:\Calendar -User Default -AccessRights LimitedDetails`.
- External sharing policy: `Set-SharingPolicy`, `Get-SharingPolicy`.
- Organization relationship for cross-tenant free/busy: `New-OrganizationRelationship -DomainNames partner.com -FreeBusyAccessEnabled $true -FreeBusyAccessLevel LimitedDetails`.
- Calendar publishing to the web is controlled by the sharing policy.

## Gotchas
- Calendar folder name is locale-dependent.
- Publishing external feeds exposes data; review quarterly.

## Self-check
Free/busy lookup from the partner tenant shows the expected detail level.
