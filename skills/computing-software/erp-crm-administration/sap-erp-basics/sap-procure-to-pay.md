---
id: computing-software.erp-crm-administration.sap-erp-basics.sap-procure-to-pay
name: sap-procure-to-pay
category: computing-software
field: erp-crm-administration
product: sap-erp-basics
tags: [sap-erp-basics, sap-mm-sd-process, sap-procure-to-pay]
level: practitioner
status: draft
description: "Follow purchase requisition to payment."
sources: ['https://help.sap.com/']
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Run the procure-to-pay flow
**Goal:** Follow purchase requisition to payment.

- ME21N creates a purchase order; MIGO posts goods receipt (movement type 101); MIRO posts the supplier invoice; payment via F110.
- Three-way match checks PO, GR and invoice.
- MMBE shows stock.

## Gotchas
- Invoice variance beyond tolerance blocks payment.

## Self-check
PO, GR and invoice documents link in the document flow.
