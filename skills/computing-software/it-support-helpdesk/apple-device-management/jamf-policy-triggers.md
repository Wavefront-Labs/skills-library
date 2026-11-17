---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-policy-triggers
name: jamf-policy-triggers
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-policies, jamf-policy-triggers, policy-triggers, jamf-pro]
level: practitioner
status: draft
description: "Choose Jamf Pro policy triggers (enrolment complete, login, recurring check-in, custom) and execution frequency so tasks run once, on demand or ongoing."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-policy-triggers

Goal: control when and how often a policy runs.
- Triggers: Startup, Login, Logout, Network State Change, Enrolment Complete, Recurring Check-in, Custom event name.
- Frequency: Once per computer, once per user per computer, once per day/week/month, Ongoing.
- Run a custom trigger manually: `sudo jamf policy -event installChrome`.
- Policy payloads: Packages, Scripts, Printers, Disk Encryption, Local Accounts, Restart options, Maintenance (recon).
- Self Service availability is separate from automatic triggers.
Practice: Custom triggers let one provisioning policy call many small policies in order, which makes failures easier to isolate than one huge policy with twenty payloads.
Gotcha: Ongoing plus Recurring Check-in re-runs every cycle; pair with an extension attribute or smart group exclusion so it stops once complete.
Verify:
- Policy log shows Completed with expected count.
- `jamf policy -event` run on a test Mac succeeds.
