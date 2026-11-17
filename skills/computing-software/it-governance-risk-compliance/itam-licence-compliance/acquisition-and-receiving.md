---
id: computing-software.it-governance-risk-compliance.itam-licence-compliance.acquisition-and-receiving
name: acquisition-and-receiving
category: computing-software
field: it-governance-risk-compliance
product: itam-licence-compliance
tags: [acquisition-and-receiving, asset-lifecycle-management, goods receipt, asset tag, barcode, rfid, serial number, warranty, itam-licence-compliance]
level: practitioner
status: draft
description: "Link PO to asset records at goods-in, tag with barcode or RFID, and capture serial, model and warranty at receipt."
sources:
  - https://www.iso.org/standard/68291.html
  - https://spdx.github.io/spdx-spec/
  - https://cyclonedx.org/specification/overview/
  - https://www.ntia.gov/page/software-bill-materials
  - https://openchainproject.org/
  - https://reuse.software/spec/
  - https://opensource.org/licenses
  - https://www.gnu.org/licenses/gpl-faq.html
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Acquisition, receiving and tagging

Goal: every asset is recorded the day it arrives, tied to its purchase.

Method:
1. Procurement supplies PO lines and vendor ASN (advance ship notice) to ITAM.
2. At receiving, scan serial number, assign an asset tag, and match to the PO line (three-way match: PO, delivery, invoice).
3. Capture model, serial, warranty end, cost centre, location and purchase cost.
4. Image or provision before assignment; update status to In stock.
5. Ask the vendor for a CSV of serial numbers on shipments above a threshold.

Gotchas:
- Drop-shipped devices bypass goods-in; require the vendor to ship serial data.
- Tag stickers peel; for high-value kit also record by serial.

Verify: reconcile last month's invoices to assets by count.
