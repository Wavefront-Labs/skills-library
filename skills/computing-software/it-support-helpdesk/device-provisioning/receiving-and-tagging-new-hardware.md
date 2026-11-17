---
id: computing-software.it-support-helpdesk.device-provisioning.receiving-and-tagging-new-hardware
name: receiving-and-tagging-new-hardware
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, asset-receiving, asset-tag, goods-receipt, cmdb, serial-number, autopilot]
level: practitioner
status: draft
description: "Receive new hardware properly: check against the PO, inspect, capture serials, tag consistently, create asset records with warranty data, and confirm Autopilot registration."
sources:
  - "https://www.axelos.com/certifications/itil-service-management/itil-4-practice-manager"
  - "https://learn.microsoft.com/en-us/autopilot/add-devices"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# receiving-and-tagging-new-hardware

## On delivery
1. Count boxes against the delivery note; refuse or note visibly damaged boxes on the
   courier's paperwork before signing.
2. Match delivery to the purchase order: model, quantity, configuration (CPU, RAM, SSD,
   keyboard layout).
3. Store in a secure stock room immediately; new laptops are a theft target.

## Record each item
- Scan the serial number barcode (avoid typing) and, for phones, IMEI.
- Affix the asset tag in a consistent place (e.g. bottom-left under the device, not on a
  removable panel or the battery). Tamper-evident labels for high-value kit.
- Create the asset record: tag, serial, model, PO number, supplier, cost, purchase date,
  warranty end and type, location, status "In stock".
- Pull warranty start and end from the vendor portal or API rather than assuming purchase
  date.

## Management readiness
- Check that the reseller registered Windows devices in Autopilot with the right group tag,
  and Apple devices appear in Apple Business Manager assigned to the right MDM server.
- Spot-check one unit per batch: power on to OOBE and confirm your organisation's branding.

## Discrepancies
Wrong spec or short delivery: raise with the supplier within their window and note on the
PO; do not tag and deploy wrong specs "for now".

## Gotchas
- Accessories (docks, monitors) below the asset threshold still need a record if they are
  issued to users; decide which items are tracked.
- Tags placed over vents or screws get removed during repairs.

## Verify
Every received unit has a tag, an asset record with serial and warranty dates, appears in
Autopilot/ABM, and the PO is marked received in finance.
