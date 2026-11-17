---
id: computing-software.collaboration-platform-administration.m365-security-compliance-purview.dlp-policy-creation
name: dlp-policy-creation
category: computing-software
field: collaboration-platform-administration
product: m365-security-compliance-purview
tags: [dlp-policy-creation, pv-dlp]
level: practitioner
status: draft
description: Build and tune a DLP policy for Exchange, SharePoint, OneDrive and Teams.
sources: ['https://learn.microsoft.com/en-us/purview/', 'https://learn.microsoft.com/en-us/defender-office-365/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Create a DLP policy
**Goal:** Build and tune a DLP policy for Exchange, SharePoint, OneDrive and Teams.

- Purview > Data loss prevention > Policies > Create; start from a template (for example U.S. Financial Data).
- Choose locations; conditions use sensitive info types with instance count and confidence.
- Actions: policy tips, block, override with justification, alerts.
- Start in Test mode with policy tips, then enforce.

## Gotchas
- Low confidence levels produce noise.
- Policy changes take about an hour to propagate (up to 24 hours).

## Self-check
Send a test message with sample sensitive data and see the policy match in Activity explorer.
