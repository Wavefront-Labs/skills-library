---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-extension-attributes
name: jamf-extension-attributes
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-ea, jamf-extension-attributes, extension-attributes, jamf-pro]
level: practitioner
status: draft
description: "Create Jamf Pro extension attributes with scripts, pop-ups or text inputs to capture custom inventory such as battery cycles or compliance flags."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Extension_Attributes.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-extension-attributes

Goal: add custom inventory fields.
- Settings > Computer Management > Extension Attributes; data types String, Integer, Date; input Script, Text, Pop-up, or LDAP mapping.
- Script EA output must be wrapped: `echo "<result>$value</result>"`.
- Example: `<result>$(sysctl -n machdep.cpu.brand_string)</result>`.
- Values update at the next inventory submission; use them in smart group criteria and advanced searches.
- Scripts run as root via the Jamf binary.
Practice: Name attributes by what they report, set the data type and inventory display category, and keep a short test script outside Jamf so a typo does not poison a fleet-wide recon.
Gotcha: an EA that takes seconds per Mac slows every recon fleet-wide, and missing `<result>` tags record nothing.
Verify:
- Inventory record shows the new field after recon.
- Smart group built on the EA contains the expected devices.
