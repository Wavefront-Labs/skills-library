---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-static-groups
name: jamf-static-groups
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-groups, jamf-static-groups, static-groups, jamf-pro]
level: practitioner
status: draft
description: "Use static groups for hand-picked, ring-based or exception scope in Jamf Pro and know when they beat smart groups."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Smart_Computer_Groups.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-static-groups

Goal: fixed membership for rollouts and exclusions.
- Computers > Static Computer Groups: add by serial or hostname, or via the Classic API `computergroups` endpoint.
- Typical use: pilot ring, VIP exclusions, devices awaiting investigation.
- Combine in policy scope with Exclusions to carve out static exceptions from smart-group targets.
- Document owner and expiry in the group description.
- Mobile devices have the same split (static vs smart mobile device groups).
Practice: Static groups also suit pre-staging: add serials before devices arrive so the first policy run is already scoped, then convert to a smart group once a dependable criterion exists.
Gotcha: static groups do not shrink when devices are retired unless someone removes them, so audit quarterly or exclusions will target dead records.
Verify:
- Policy log shows a pilot device running while others skip.
- Group list reviewed against retired devices.
