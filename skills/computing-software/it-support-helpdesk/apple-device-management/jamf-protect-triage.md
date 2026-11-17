---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-protect-triage
name: jamf-protect-triage
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-protect, jamf-protect-triage, protect-alerts, triage]
level: practitioner
status: draft
description: "Triage Jamf Protect alerts and use device isolation or smart groups in Jamf Pro to contain suspicious Macs."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-protect-documentation/page/Jamf_Protect_Documentation.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-protect-triage

Goal: handle detections consistently.
- Alerts show analytic, process tree, file paths and Mac user.
- Triage steps: confirm process path and signing, check recent installs, compare with allow-lists, then dismiss or escalate.
- Contain: network quarantine via smart group plus an enforcement policy (confirm product capabilities).
- Maintain an exception list for known-good admin tools, with owner and expiry.
- Record decision in the ticket.
Practice: Define severity levels with response times, and use the process tree plus signing information to separate admin tooling from malware. Close each alert with a reason code for later tuning.
Gotcha: tuning by disabling noisy analytics hides real events; add exceptions with narrow predicates instead.
Verify:
- Alert volume tracked weekly.
- Each exception has a ticket reference.
