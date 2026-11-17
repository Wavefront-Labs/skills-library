---
id: computing-software.it-support-helpdesk.apple-device-management.compliance-reporting
name: compliance-reporting
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, compliance-inventory, compliance-reporting, dashboards]
level: practitioner
status: draft
description: "Build compliance dashboards from smart groups, Advanced Searches and EAs covering encryption, patching and security settings."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Computer_Inventory.html"
  - "https://developer.apple.com/documentation/devicemanagement/deviceinformation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# compliance-reporting

Goal: prove device posture.
- Define checks: FileVault on, OS at or above target, Firewall on, SIP enabled, EDR running.
- Smart groups flag failures; Advanced Search exports CSV.
- Use the Jamf Pro API for data to SIEM or BI.
- Alert on non-compliant counts with notifications.
- Store history monthly.
Practice: Agree the pass criteria with security, report weekly, and show trends rather than a single snapshot so stakeholders see whether remediation is working. Keep the query definitions in documentation so results can be reproduced.
Gotcha: stale inventory looks like non-compliance; include Last Check-in in reports.
Note: Share a one-page summary with managers listing top failing controls and the plan to fix them.
Verify:
- Report totals match fleet size.
- Failing devices have owners.
