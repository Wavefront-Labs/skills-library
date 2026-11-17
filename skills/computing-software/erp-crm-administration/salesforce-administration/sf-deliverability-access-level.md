---
id: computing-software.erp-crm-administration.salesforce-administration.sf-deliverability-access-level
name: sf-deliverability-access-level
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-email-deliverability, sf-deliverability-access-level]
level: practitioner
status: draft
description: "Control outbound email from the org."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set email deliverability access level
**Goal:** Control outbound email from the org.

- Setup > Deliverability: No access, System email only, All email; sandboxes default to System email only.
- Set organisation-wide email addresses and SPF/DKIM for custom domains.
- Verify bounce handling.

## Gotchas
- Sandbox refresh resets the level to System email only.

## Self-check
Test email delivers in the intended environment.
