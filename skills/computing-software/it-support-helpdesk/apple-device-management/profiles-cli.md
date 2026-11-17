---
id: computing-software.it-support-helpdesk.apple-device-management.profiles-cli
name: profiles-cli
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, client-troubleshooting, profiles-cli, profiles-command]
level: practitioner
status: draft
description: "Use the profiles command to list, show, renew and remove configuration profiles and check enrolment status."
sources:
  - "https://support.apple.com/guide/deployment/welcome/web"
  - "https://developer.apple.com/documentation/devicemanagement"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# profiles-cli

Goal: inspect MDM state locally.
- `sudo profiles list`, `profiles show -all`, `profiles status -type enrollment`.
- Renew enrolment: `sudo profiles renew -type enrollment`.
- Remove: `sudo profiles remove -identifier com.example`.
- Trigger ADE: `sudo profiles renew -type enrollment`.
- Export with `profiles -P -o file.plist`.
Practice: Run `profiles` as root, compare the identifier list with what the MDM thinks is installed, and capture output with a timestamp when opening a ticket with the vendor. Save the output of `profiles list -output stdout-xml` for comparison after changes.
Gotcha: `profiles -D` removes all profiles; never run it on managed devices.
Note: On macOS 11 and later, profiles can be listed only by root, so use sudo in remote shells and scripts.
Verify:
- Expected profile identifiers appear.
- Enrolment status shows MDM enrolment yes.
