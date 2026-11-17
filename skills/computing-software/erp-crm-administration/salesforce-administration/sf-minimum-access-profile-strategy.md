---
id: computing-software.erp-crm-administration.salesforce-administration.sf-minimum-access-profile-strategy
name: sf-minimum-access-profile-strategy
category: computing-software
field: erp-crm-administration
product: salesforce-administration
tags: [salesforce-administration, sf-minimum-access-profile-strategy]
level: advanced
status: draft
description: "Use a minimum-access profile and grant everything through permission sets."
sources: ['https://help.salesforce.com/', 'https://trailhead.salesforce.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Keep profiles minimal and grant through permission sets
**Goal:** Use a minimum-access profile and grant everything through permission sets.

- Clone Minimum Access - Salesforce profile for new users; add object, field and system permissions only through permission sets.
- Salesforce has announced a direction away from permissions on profiles (confirm the current retirement schedule in release notes).
- Audit with the Permission Set and Profile reports and the Security Health Check.

## Gotchas
- Do not edit standard profiles to add custom access; it is hard to audit.

## Self-check
Removing a permission set removes exactly the access it granted.
