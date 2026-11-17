---
id: computing-software.it-support-helpdesk.intune-mdm.jamf-pro-policies
name: jamf-pro-policies
category: computing-software
field: it-support-helpdesk
product: intune-mdm
tags: [it-support-helpdesk, intune-mdm, jamf, jamf-pro, jamf-policies, policy-triggers, execution-frequency, jamf-scope, jamf-binary, jamf-policy-logs, macos-management, jamf-scripts]
level: practitioner
status: draft
description: "Build and debug Jamf Pro policies: triggers, execution frequency, scope and exclusions, packages and scripts payloads, and reading policy logs on server and client."
sources:
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policy_Management.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Scope.html"
  - "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Policy_Logs.html"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# jamf-pro-policies

Goal: Mac software, scripts and settings tasks run exactly once (or as
often as intended) on exactly the right Macs.

## Anatomy
- **General**: name, category, **trigger** and **execution frequency**.
- **Payloads**: Packages, Scripts, Printers, Maintenance (inventory update),
  Files and Processes, Local accounts, Restart, etc.
- **Scope**: targets (computers, smart/static groups, buildings,
  departments), **limitations** (users/network segments) and
  **exclusions**.
- **Self Service**: optionally make the policy user-triggered from the
  Self Service app.

## Triggers
| Trigger | Fires when |
|---|---|
| Recurring Check-in | every client check-in (default 15 min) |
| Enrollment Complete | right after enrolment (zero-touch app installs) |
| Startup / Login / Logout | system events |
| Network State Change | IP changes |
| Custom | `sudo jamf policy -event <name>` — chain policies from scripts |
Execution frequency: Once per computer, Once per user per computer, Once
every day/week/month, Ongoing. "Ongoing + recurring check-in" runs every 15
minutes forever — only for idempotent, cheap tasks.

## Client-side commands
```bash
sudo jamf policy                      # run check-in policies now
sudo jamf policy -event install-zoom  # custom trigger
sudo jamf policy -id 123              # run a specific policy (testing)
sudo jamf recon                       # update inventory
sudo jamf checkJSSConnection
tail -f /var/log/jamf.log
```

## Debugging "it didn't run"
1. Computer record → History → **Policy Logs**: Completed / Failed /
   Pending with full output.
2. Is the Mac in scope? Smart group membership updates at inventory
   (`recon`), not instantly — stale inventory = wrong scope.
3. Exclusions win over targets.
4. Frequency already satisfied ("Once per computer") — flush the policy log
   for that computer (Policy → Logs → Flush) to rerun.
5. Package not on distribution point / cloud DP sync failure.
6. Script exit code non-zero = Failed even if it "worked".

## Gotchas
- Policies run as root; user context needs `launchctl asuser` or a
  `$3` (current user) parameter in scripts.
- Install packages by "Install" action with "Update inventory" in
  Maintenance, or smart groups lag.
- Don't scope to "All Computers" while testing — use a test static group.

## Verify
Policy log shows Completed for target Macs, inventory reflects the change
(app version / EA), and no unexpected Macs ran it.
