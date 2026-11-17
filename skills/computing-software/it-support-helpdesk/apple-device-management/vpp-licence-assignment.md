---
id: computing-software.it-support-helpdesk.apple-device-management.vpp-licence-assignment
name: vpp-licence-assignment
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, vpp-apps, vpp-licence-assignment, vpp, licence-assignment, apps-and-books]
level: practitioner
status: draft
description: "Purchase and assign Apps and Books licences in ABM with device-based assignment, location tokens and licence reclaim."
sources:
  - "https://support.apple.com/guide/apple-business-manager/welcome/web"
  - "https://support.apple.com/guide/deployment/distribute-apps-and-books-dep9b8c8a9b7/web"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# vpp-licence-assignment

Goal: deploy store apps without personal Apple Accounts.
- Buy in ABM > Apps and Books by location; choose quantity and custom apps if needed.
- Device-based assignment installs silently without a user Apple Account; user-based needs Managed Apple Accounts.
- Add the location token in Jamf Pro under Settings > Global > Volume Purchasing; sync and scope apps.
- Reclaim licences by removing scope or switching assignment.
- Free apps still need a licence assignment.
Practice: Keep a naming and location convention, review licence counts before large rollouts, and remember custom apps and B2B apps use the same assignment process.
Gotcha: one token can only be tied to one MDM at a time; moving it silently breaks app installs on the old server.
Verify:
- App shows licence count remaining.
- Test device installs the app silently.
