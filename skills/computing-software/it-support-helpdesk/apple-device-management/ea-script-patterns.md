---
id: computing-software.it-support-helpdesk.apple-device-management.ea-script-patterns
name: ea-script-patterns
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-ea, ea-script-patterns, ea-scripts, shell]
level: practitioner
status: draft
description: "Write reliable EA scripts for compliance checks such as FileVault, pending updates and last reboot, with fast, safe commands and empty-value handling."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Extension_Attributes.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ea-script-patterns

Goal: reusable EAs that stay fast and valid.
- FileVault: `fdesetup status | head -1` returned inside result tags.
- Uptime days: `echo "<result>$(( ( $(date +%s) - $(sysctl -n kern.boottime | awk -F'[ ,]+' '{print $4}') ) / 86400 ))</result>"`.
- Pending updates: parse `softwareupdate -l` only if cached; avoid network calls in EAs (confirm behaviour).
- Always default: `value=${value:-Unknown}`.
- Prefer built-in tools (`defaults`, `profiles`, `dscl`) over installing dependencies.
- Test locally with `sudo bash ea.sh` before pasting into Jamf.
Gotcha: running a network-bound command inside an EA can time out the whole inventory submission.
Verify:
- Script returns a single result block in under a second.
- Value appears in inventory for a test Mac.
