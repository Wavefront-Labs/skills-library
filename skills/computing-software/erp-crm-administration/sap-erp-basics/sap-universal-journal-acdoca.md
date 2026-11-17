---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-universal-journal-acdoca
name: sap-universal-journal-acdoca
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-universal-journal-acdoca]
level: advanced
status: draft
description: "Know where financial line items live in S/4HANA."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Understand the universal journal
**Goal:** Know where financial line items live in S/4HANA.

- ACDOCA is the universal journal line item table combining FI and CO postings; reports read it directly.
- Many ECC aggregate tables are replaced by views.
- Check conversion simplification items.

## Gotchas
- Custom code referencing removed tables breaks; run the code check.

## Self-check
Journal entries show in ACDOCA after a test posting.
