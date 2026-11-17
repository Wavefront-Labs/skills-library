---
id: computing-software.it-support-helpdesk.apple-device-management.inventory-collection
name: inventory-collection
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, compliance-inventory, inventory-collection, inventory, recon-settings]
level: practitioner
status: draft
description: "Configure what Jamf Pro collects at recon and how DeviceInformation queries refresh iOS inventory."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Inventory.html"
  - "https://developer.apple.com/documentation/devicemanagement/deviceinformation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# inventory-collection

Goal: accurate, timely records.
- Settings > Computer Management > Inventory Collection: software, services, fonts, plugins, local users.
- Set inventory frequency via policy with Update Inventory.
- Mobile devices use periodic DeviceInformation commands.
- Reduce collection of heavy items to speed recon.
- Use Advanced Searches to export.
Practice: Match collection to the questions you need answered, such as installed software and local accounts, and disable the rest to keep inventory fast and the database small. Review these settings when Jamf releases new collection options.
Gotcha: collecting all applications on large fleets slows submission; limit to needed paths.
Note: Export a sample record after changing settings to confirm the new fields populate as expected.
Verify:
- Last inventory update is recent.
- Advanced search returns expected fields.
