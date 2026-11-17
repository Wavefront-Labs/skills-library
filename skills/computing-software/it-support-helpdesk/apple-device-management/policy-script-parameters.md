---
id: computing-software.it-support-helpdesk.apple-device-management.policy-script-parameters
name: policy-script-parameters
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-scripts, policy-script-parameters, scripts, parameters]
level: practitioner
status: draft
description: "Use the Jamf Pro script parameter conventions ($1 to $11, $3 user) and variables so one script serves many policies."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Scripts.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# policy-script-parameters

Goal: write reusable policy scripts.
- Jamf passes $1 mount point, $2 computer name, $3 username; parameters 4 to 11 are yours.
- Set labels in the script record so policy editors know what to enter.
- Get console user safely: `stat -f%Su /dev/console` (or `scutil` ConsoleUser key); never trust `$USER` under root.
- Run priority Before/After the package install.
- Exit non-zero on failure so the policy log shows Failed.
Practice: Document parameter meanings in the script record labels and in a header comment, and prefer parameters to hard-coded values so one tested script serves pilot and production.
Gotcha: a missing parameter arrives as empty string; validate with `[ -z "$4" ] && exit 1`.
Verify:
- Policy log shows the script output.
- Changing a parameter changes behaviour without editing the script.
