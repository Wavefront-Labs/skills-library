---
id: computing-software.systems-network-administration.windows-server.deploy-printers-by-group-policy
name: deploy-printers-by-group-policy
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, print-server, print-services, deployed-printers, group-policy-preferences, item-level-targeting, shared-printer, default-printer]
level: practitioner
status: docs-checked
description: "Deploy printers to users and computers with Group Policy: GPP shared printer items, item-level targeting, default printer, Print Management deployment and cleanup."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-preferences
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/group-policy-printer-preferences-not-set-default-printer
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/pushprinterconnections
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Deploy printers by Group Policy

## Group Policy Preferences (preferred)
User Configuration > Preferences > Control Panel Settings > Printers > New > **Shared
Printer**:
- Action: **Update**. Note that *Remove this item when it is no longer applied* forces the action to Replace (delete and
  recreate as needed).
- Share path: `\\PRINT01\Floor2-Color`.
- Default printer: setting the default can fail the first time a user logs on, because the printer connection is not
  registered until the logon completes (see the Troubleshoot section).
- Common tab > **Item-level targeting**: security group, IP address range, site, OU, computer name, and more. One GPO,
  many printers, each targeted.
- Common tab > **Run in logged-on user's security context**: user preference items run as SYSTEM by default; select this
  option when the item needs the user's resources (such as network connections).

Group Policy Printers can create, modify or delete TCP/IP, shared and local printer connections.

## Print Management "Deploy with Group Policy"
Older method: Print Management > right-click printer > Deploy with Group Policy. `pushprinterconnections.exe` reads
the Deployed Printer Connection settings from Group Policy and is meant for machine startup or user logon scripts, not
for running from the command line (`-log` writes a debug log). Less flexible than GPP targeting.

## Removing printers
Change the item action to **Delete** for a refresh cycle, or select "Remove this item when it is no longer applied"
before unlinking (not available when the action is Delete).

## Troubleshoot
- `gpresult /h report.html` shows which GPOs applied.
- Application log event 4098: for example `0x80070709 The printer name is invalid` when a default-printer item runs
  before the connection exists at first logon.
- `Get-Printer` as the user shows connections.

## Verify
- [ ] Targeted user gets the right printers after `gpupdate` and logon; others do not.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: Group Policy Printers covers TCP/IP, shared and local printers; the common options (Run in logged-on user's security context runs user items as SYSTEM by default, Remove this item sets Replace and is unavailable with Delete); item-level targeting types (security group, OU, site, computer name, IP address range); the pushprinterconnections purpose and -log switch; event 4098 with error 0x80070709 and the first-logon default printer cause. Fixed: the skill stated that logon-user context is the default for user items; the documentation says user items run as SYSTEM by default. Removed as unconfirmed: Point and Print and package-aware driver advice (the support article is not readable), error 0x80070bcb, the Replace flicker claim, and the claim that Print Management deployment still works without pushprinterconnections.

Method: documentation only; no commands were run.
