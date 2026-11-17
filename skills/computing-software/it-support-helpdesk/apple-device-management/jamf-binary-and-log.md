---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-binary-and-log
name: jamf-binary-and-log
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-troubleshooting, jamf-binary-and-log, jamf-binary, jamf-log]
level: practitioner
status: draft
description: "Use the jamf binary to run policies, recon and repair the framework, and read the jamf log."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Troubleshooting.html"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-binary-and-log

Goal: diagnose agents on a Mac.
- `sudo jamf policy -verbose`, `sudo jamf recon`, `sudo jamf manage`.
- Log: `/var/log/jamf.log`.
- Check connection: `sudo jamf checkJSSConnection`.
- Repair: `sudo jamf removeFramework` then re-enrol (last resort).
- Check the daemon: `launchctl list | grep jamf`.
Practice: Rotate and collect `jamf.log` from affected Macs, search for the policy name, and compare the policy log on the server with the local log to see where the run stopped. Use `sudo jamf log` style helpers or Console to follow the log live during testing.
Gotcha: removing the framework does not remove MDM enrolment; ensure the profile too.
Note: If the daemon is unhealthy, check the LaunchDaemon plist and the Jamf binary version before reinstalling anything.
Verify:
- Policy runs end to end.
- Check-in time updates.
