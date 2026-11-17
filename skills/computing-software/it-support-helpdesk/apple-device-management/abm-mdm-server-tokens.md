---
id: computing-software.it-support-helpdesk.apple-device-management.abm-mdm-server-tokens
name: abm-mdm-server-tokens
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, abm-setup, abm-mdm-server-tokens, token, mdm-server]
level: practitioner
status: draft
description: "Link Jamf or another MDM to Apple Business Manager with server tokens, rotate expiring tokens and reassign devices between servers without losing enrolment."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://support.apple.com/guide/deployment/welcome/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# abm-mdm-server-tokens

Goal: keep the ABM-to-MDM link healthy.
- Settings > Device Management Settings > Add MDM Server: name it, upload the MDM public key, download the encrypted `.p7m` token and import it into the MDM (Jamf Pro: Computers > Automated Device Enrollment).
- Tokens expire after one year; renew by downloading a new token for the same server record, not by adding a second server.
- Assign devices by serial, order number or CSV (Devices > Edit Device Management); choose the target server and save.
- Terms and conditions must be re-accepted by an Administrator after changes or sync stops.
Gotcha: a new server record means a new token and a different default profile set; devices stay on the old server until reassigned, and an expired token silently stops new assignments.
Verify:
- MDM shows token expiry and last sync time.
- A test serial appears in the MDM device list after assignment.
- Token renewal date is in the team calendar.
