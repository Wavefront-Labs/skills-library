---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.service-health-incidents
name: service-health-incidents
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [service-health-incidents, m365-service-health]
level: practitioner
status: draft
description: Track incidents and advisories and subscribe to notifications.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Service health and incidents
**Goal:** Track incidents and advisories and subscribe to notifications.

- Admin center > Health > Service health shows incidents and advisories with a per-service status.
- Email notifications: Service health > Preferences; add recipients per issue type.
- Graph: `GET /admin/serviceAnnouncement/issues` (needs ServiceHealth.Read.All).
- Record the incident ID (e.g. EX1234567) when raising a support request.

## Gotchas
- Status shown in the portal can lag a real outage; check the public @MSFT365Status feed too.
- Notification emails go only to roles with the permission.

## Self-check
Send a test notification setting and confirm the recipient receives issue emails.
