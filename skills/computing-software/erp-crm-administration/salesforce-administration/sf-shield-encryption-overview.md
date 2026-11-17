---
id: computing-software.erp-crm-administration.salesforce-administration.sf-shield-encryption-overview
name: sf-shield-encryption-overview
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-shield-encryption-overview]
level: advanced
status: draft
description: "Choose between classic encrypted text fields and Shield Platform Encryption."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand Shield Platform Encryption and classic encryption
**Goal:** Choose between classic encrypted text fields and Shield Platform Encryption.

- Classic encrypted custom text fields (Encrypted text) use a masked value; limited functionality.
- Shield Platform Encryption is a licensed add-on, encrypts standard and custom fields at rest with tenant secrets, and has feature trade-offs (search, filters).
- Plan key management and backup of tenant secrets.

## Gotchas
- Losing key material makes data unreadable.

## Self-check
Encrypted fields are listed in Setup > Platform Encryption after enabling.
