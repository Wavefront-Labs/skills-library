---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.endpoint-dlp
name: endpoint-dlp
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [endpoint-dlp]
level: advanced
status: draft
description: Protect data on onboarded Windows and macOS devices.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Endpoint DLP
**Goal:** Protect data on onboarded Windows and macOS devices.

- Devices must be onboarded (Defender for Endpoint or Intune); enable in Settings > Device onboarding.
- Rules for copy to USB, cloud upload, print and paste into browsers.
- Define allowed browsers, service domains and file path exclusions.
- Review events in Activity explorer.

## Gotchas
- Unsupported apps bypass restrictions; use the restricted apps list.
- Performance impact must be validated on pilot machines.

## Self-check
Copying a labelled test file to USB is blocked with the notification.
