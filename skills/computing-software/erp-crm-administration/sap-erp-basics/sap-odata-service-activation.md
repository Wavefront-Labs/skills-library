---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-odata-service-activation
name: sap-odata-service-activation
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-odata-service-activation]
level: advanced
status: draft
description: "Make Fiori apps' back-end services available."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Activate OData services
**Goal:** Make Fiori apps' back-end services available.

- /IWFND/MAINT_SERVICE adds and activates services on the gateway; check ICF node status.
- Error log in /IWFND/ERROR_LOG; clear caches after changes.
- Add services to authorisations via roles.

## Gotchas
- Service activation requires matching authorisation objects (S_SERVICE).

## Self-check
App data loads with no service errors.
