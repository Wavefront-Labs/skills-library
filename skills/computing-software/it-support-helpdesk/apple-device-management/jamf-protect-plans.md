---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-protect-plans
name: jamf-protect-plans
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-protect, jamf-protect-plans, plans]
level: practitioner
status: draft
description: "Configure Jamf Protect plans with analytic sets, actions and removable storage controls on managed Macs via the Protect console and Jamf Pro."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-protect-documentation/page/Jamf_Protect_Documentation.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-protect-plans

Goal: deploy endpoint detection tuned to your fleet.
- Plans bundle Analytic Sets, Actions (log, alert, quarantine), Telemetry and Removable Storage controls.
- Import default analytics or write your own using predicates; test in Log Only before alert-only.
- Deploy the agent and plan via Jamf Pro profile and pkg with system extension and TCC approval.
- Forward alerts to SIEM through HTTP or cloud storage.
- Name plans by ring: Pilot, Standard.
Practice: Roll plans out in rings, review telemetry volume and storage costs before enabling verbose categories, and keep the Jamf Protect extension approval profile versioned with the agent package.
Gotcha: the system extension and full-disk-access approval must be pushed before the agent installs, or it sits inactive.
Verify:
- Agent status Connected in the console.
- A benign test analytic triggers an alert.
