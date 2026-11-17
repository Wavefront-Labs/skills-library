---
id: computing-software.networking-hardware-and-wireless.network-device-administration.nda-device-inventory-and-lifecycle-tracking
name: nda-device-inventory-and-lifecycle-tracking
category: computing-software
field: networking-hardware-and-wireless
product: network-device-administration
tags: [network-inventory-eol, support-contract-tracking, license-management]
level: intro
status: draft
description: "Maintain an inventory of models, serials, firmware, contract expiry and vendor end-of-life dates to plan refresh."
sources:
  - https://www.cisco.com/
  - https://www.juniper.net/documentation/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Inventory and lifecycle

- Fields: hostname, role, model, serial, firmware, location, IPs, contract end, licence type and expiry, EoL/EoS dates, owner.
- Pull data automatically (SNMP entity MIB, vendor APIs, controllers) and reconcile with finance records.
- Watch vendor end-of-sale, end-of-software-maintenance and end-of-support notices; plan replacement 12-18 months before last support.
- Cloud-managed licences can disable features at expiry; set renewals early.

## Verify
- [ ] A report lists every device with contract end date and flags those expiring within 180 days.
