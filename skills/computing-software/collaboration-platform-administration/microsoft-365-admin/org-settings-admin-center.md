---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.org-settings-admin-center
name: org-settings-admin-center
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [org-settings-admin-center, m365-org-settings]
level: practitioner
status: draft
description: 'Configure Settings > Org settings: security and privacy, services and add-ins, tenant branding.'
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Org-wide settings in the admin center
**Goal:** Configure Settings > Org settings: security and privacy, services and add-ins, tenant branding.

- Settings > Org settings has Services (e.g. Microsoft 365 on the web, Calendar, Forms, Bookings) and Security & privacy (password expiration, idle session timeout, sharing).
- Idle session timeout signs users out of web apps after inactivity; set deliberately.
- Customize the admin center nav and use the admin center's search to jump to settings.
- Changes can take up to a few hours to apply; note the change in a change log.

## Gotchas
- Many settings overlap with Entra and per-service admin centers; the most restrictive wins, so document where each is set.
- Password expiration is discouraged by current NIST guidance; leave as never expires with MFA (policy choice).

## Self-check
Re-open the setting after saving and confirm the value persisted.
