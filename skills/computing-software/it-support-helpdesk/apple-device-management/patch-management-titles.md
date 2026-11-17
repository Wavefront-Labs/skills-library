---
id: computing-software.it-support-helpdesk.apple-device-management.patch-management-titles
name: patch-management-titles
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-patch, patch-management-titles, patch-management, titles]
level: practitioner
status: draft
description: "Add patch software titles in Jamf Pro, subscribe to a patch source and use reporting to see which Macs are on which version."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Patch_Management.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# patch-management-titles

Goal: track app versions across the fleet.
- Computers > Patch Management > New: choose a software title from the Jamf patch server or an external source.
- The title definition maps versions to detection via application bundle ID or EA.
- Dashboard shows Up to Date, Out of Date, Unknown.
- Patch reporting depends on inventory freshness.
Practice: Add titles for the apps users actually run, review their detection definitions after each vendor release, and use reporting to feed the update calendar and exceptions list.
Gotcha: Unknown counts arise when detection uses the app name rather than bundle ID, or when inventory excludes a path; check the definition.
Verify:
- Counts match a manual app search.
- Version list updates after the source syncs.
