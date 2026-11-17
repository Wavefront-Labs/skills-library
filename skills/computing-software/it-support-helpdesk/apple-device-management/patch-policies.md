---
id: computing-software.it-support-helpdesk.apple-device-management.patch-policies
name: patch-policies
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-patch, patch-policies, deadlines]
level: practitioner
status: draft
description: "Create Jamf Pro patch policies to install new versions through Self Service or automatically with deadlines and grace periods."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Patch_Management.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# patch-policies

Goal: update apps without manual packaging.
- Patch policy takes a package per version, scope, and user interaction settings.
- Deadlines: notify user with grace period, then force-quit and update.
- Self Service option lets users update early.
- Use a pilot smart group first, then widen.
- Pair with Installomator scripts when no pkg exists (see installomator).
Practice: Keep one policy per title and ring, set a realistic deadline, and send a clear message about quitting the app, so forced updates do not destroy unsaved work.
Gotcha: patch policies need a package uploaded per version; missing versions leave the policy idle until you add one.
Verify:
- A test Mac updates and reports the new version.
- Policy log shows version number.
