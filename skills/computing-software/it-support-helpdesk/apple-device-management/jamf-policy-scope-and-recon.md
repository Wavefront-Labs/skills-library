---
id: computing-software.it-support-helpdesk.apple-device-management.jamf-policy-scope-and-recon
name: jamf-policy-scope-and-recon
category: computing-software
field: it-support-helpdesk
product: apple-device-management
tags: [it-support-helpdesk, apple-device-management, jamf-policies, jamf-policy-scope-and-recon, scope, exclusions, recon]
level: practitioner
status: draft
description: "Scope Jamf Pro policies with targets, limitations and exclusions, and make inventory update after a policy so smart groups stay accurate."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policies.html"
  - "https://learn.jamf.com/"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# jamf-policy-scope-and-recon

Goal: reach exactly the right Macs and refresh state afterwards.
- Scope tabs: Targets (computers, groups, departments, buildings), Limitations (users, network segments), Exclusions (override targets).
- Add a Maintenance payload with Update Inventory so group membership refreshes after install.
- `sudo jamf recon` forces inventory now; `sudo jamf policy` runs pending check-in policies.
- Use Smart Group exclusions like "Has Chrome current" to make install policies idempotent.
- Review policy logs under the policy's Logs button for per-computer status.
Practice: Prefer department or building scope for regional rules and groups for state-based rules, and review the scope of broad policies whenever someone adds an exclusion.
Gotcha: exclusions beat targets, so an exclusion group left on a policy silently blocks everyone in it.
Verify:
- Scope preview count matches expectations.
- Inventory reflects the change after the policy runs.
