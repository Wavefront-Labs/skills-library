---
id: computing-software.erp-crm-administration.dynamics-365-administration.dyn-dlp-capacity
name: dyn-dlp-capacity
category: computing-software
field: erp-crm-administration
product: dynamics-365-administration
tags: [dynamics-365-administration, dyn-dlp-capacity]
level: advanced
status: draft
description: "Control connectors and track storage."
sources: ['https://learn.microsoft.com/en-us/dynamics365/', 'https://learn.microsoft.com/en-us/power-platform/admin/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Apply DLP policies and monitor capacity
**Goal:** Control connectors and track storage.

- Data policies group connectors into Business, Non-business and Blocked.
- Capacity reports show database, file and log storage by environment.
- Set tenant and environment policies.

## Gotchas
- Policy changes can break existing flows using blocked connector combinations.

## Self-check
A flow using a blocked connector is flagged.
