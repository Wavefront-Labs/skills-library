---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-script-best-practices
name: jamf-script-best-practices
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-scripts, jamf-script-best-practices, script-best-practices, idempotent]
level: practitioner
status: draft
description: "Write safe, idempotent Jamf scripts with logging, quoting and error handling, and test them locally before scoping."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Scripts.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-script-best-practices

Goal: scripts that are safe to rerun at scale.
- Start with `#!/bin/zsh`, `set -u`, and a `log()` function writing to `/var/log` or syslog via `logger`.
- Check before acting (`[ -d "/Applications/App.app" ] && exit 0`).
- Quote variables and avoid `sudo` inside scripts as policies run as root.
- Do not embed passwords; use API clients or the jamf binary.
- Test on a VM with `sudo zsh script.sh param4`.
- Keep scripts in git and upload from the repo.
Practice: Add a version comment and a dry-run switch, lint with shellcheck and keep a test VM snapshot to rerun against, so changes are proven before they reach the fleet.
Gotcha: scripts that prompt for input hang the policy; use jamfHelper or swiftDialog with a timeout.
Verify:
- Second run exits cleanly without changes.
- Log file shows readable steps.
