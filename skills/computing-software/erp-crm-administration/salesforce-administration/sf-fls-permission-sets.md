---
id: computing-software.erp-crm-administration.salesforce-administration.sf-fls-permission-sets
name: sf-fls-permission-sets
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-field-level-security, sf-fls-permission-sets]
level: practitioner
status: draft
description: "Control read and edit on individual fields."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Set field-level security with permission sets
**Goal:** Control read and edit on individual fields.

- Field-level security is set per profile and permission set; Read-only or hidden hides it from page layouts, reports, list views and APIs.
- Page layout field settings only affect UI; use FLS for data protection.
- Use the field's Set Field-Level Security screen and the Field Accessibility viewer.

## Gotchas
- Required fields in layouts still need FLS access or the user cannot save.

## Self-check
The API and reports hide the field for a user lacking FLS.
