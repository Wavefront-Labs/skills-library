---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-smart-groups
name: jamf-smart-groups
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-groups, jamf-smart-groups, smart-groups, jamf-pro]
level: practitioner
status: draft
description: "Build Jamf Pro smart groups with criteria, and/or logic and nested groups, and avoid slow, stale or circular membership."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Smart_Computer_Groups.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-smart-groups

Goal: dynamic scope that updates from inventory.
- Computers > Smart Computer Groups > New; criteria such as Operating System Version less than 15.2, Last Check-in more than 30 days ago, Application Title, or an extension attribute.
- Use "Member of" to nest groups; group the "and" conditions before "or" with parentheses.
- Membership recalculates on inventory submission, so a policy depending on a fresh result needs recon first.
- Name groups by purpose, such as `SG - macOS below 15.2`.
- Enable notifications on membership change only for alerts, as they add load.
Gotcha: circular nesting or heavy criteria like Application Title with wildcards slows recalculation and delays policy scope.
Verify:
- Group count matches a manual inventory search.
- A test Mac moves in and out after a recon.
