---
id: computing-software.it-support-helpdesk.apple-device-management.mdmclient-and-logs
name: mdmclient-and-logs
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, client-troubleshooting, mdmclient-and-logs, mdmclient, unified-log]
level: practitioner
status: draft
description: "Trigger check-in and read MDM logs with mdmclient and the unified log."
sources:
  - "https://support.apple.com/guide/deployment/welcome/web"
  - "https://developer.apple.com/documentation/devicemanagement"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# mdmclient-and-logs

Goal: see what the device receives.
- `sudo /usr/libexec/mdmclient QueryInstalledProfiles`, `QueryDeviceInformation`.
- Log: `log show --last 30m --predicate 'process == "mdmclient"'`.
- Force check-in: `sudo /usr/libexec/mdmclient checkin` (confirm).
- Use Console filtering.
- Check network connectivity to APNs.
Practice: Filter the log to the minimum window around the test, redact device identifiers before sharing, and compare timestamps with the MDM command history to find where the exchange stalled. Remember that command output may need sudo to show enrolment details.
Gotcha: mdmclient output differs per macOS version.
Note: Keep a short reference of the log predicates your team uses so every technician captures the same evidence.
Verify:
- Log shows command received and acknowledged.
- Device returns data.
