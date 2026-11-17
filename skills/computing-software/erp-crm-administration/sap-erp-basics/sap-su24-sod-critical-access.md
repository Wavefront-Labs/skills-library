---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-su24-sod-critical-access
name: sap-su24-sod-critical-access
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-su24-sod-critical-access]
level: advanced
status: draft
description: "Review dangerous authorisations and segregation of duties."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Detect critical authorisations
**Goal:** Review dangerous authorisations and segregation of duties.

- SU24 maintains default authorization values by transaction; SUIM can list who has S_TCODE or S_DEVELOP and profiles such as SAP_ALL.
- Restrict SAP_ALL and debug-with-replace (S_DEVELOP activity 02) authorisations in production.
- Use GRC Access Control or SoD rule sets where licensed.

## Gotchas
- SAP_ALL grants all authorisations; restrict it to emergency use with logging.

## Self-check
A report of users with critical profiles is produced and reviewed.
