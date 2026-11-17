---
id: computing-software.collaboration-platform-administration.microsoft-365-admin.update-channels-cloud-policy
name: update-channels-cloud-policy
category: computing-software
field: collaboration-platform-administration
product: microsoft-365-admin
tags: [update-channels-cloud-policy]
level: practitioner
status: draft
description: Choose Current, Monthly Enterprise or Semi-Annual Enterprise channel and manage settings by cloud policy.
sources: ['https://learn.microsoft.com/en-us/microsoft-365/admin/', 'https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/ms-102']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Update channels and Cloud Policy
**Goal:** Choose Current, Monthly Enterprise or Semi-Annual Enterprise channel and manage settings by cloud policy.

- Channels: Current Channel, Monthly Enterprise Channel, Semi-Annual Enterprise Channel (confirm names in current docs).
- Change channel by XML `<Add Channel=...>` or an update policy.
- Config.office.com > Customization > Policy Management applies cloud policy to signed-in users.
- Admin center > Settings > Microsoft 365 Apps > Inventory and Servicing profiles in Apps admin center for update deadlines.

## Gotchas
- Switching to a more stable channel may not downgrade the build; plan a reinstall.
- Policies apply when the user signs in; offline devices lag.

## Self-check
Verify the channel and version in File > Account > About.
