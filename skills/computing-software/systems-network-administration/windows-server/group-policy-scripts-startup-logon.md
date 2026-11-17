---
id: computing-software.systems-network-administration.windows-server.group-policy-scripts-startup-logon
name: group-policy-scripts-startup-logon
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, gp-advanced-settings, logon-scripts, startup-scripts, powershell-scripts, group-policy]
level: practitioner
status: docs-checked
description: "Deploy startup, shutdown, logon and logoff scripts with Group Policy: where to store them, PowerShell scripts, timing, run-as context and troubleshooting."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-client/group-policy/logon-scripts-not-run-for-long-time
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Group Policy startup and logon scripts

## Types and context
| Script | Runs as | When |
|---|---|---|
| Startup / Shutdown | computer policy | computer start / shutdown |
| Logon / Logoff | user policy | user logon / logoff |
Edit: Computer or User Configuration > Policies > Windows Settings > Scripts. Group Policy processes the script
extension during background refresh, but an individual script runs only at startup, shutdown, logon or logoff.

## Store them in the GPO
Store scripts where the target computers and users can read them, for example in the GPO's folder under SYSVOL
(`\\<dcName>\SYSVOL\<domain>\Policies\<guid>\`), so they replicate with the GPO.

## Timing gotchas
- **Logon script delay**: on Windows 8.1 and later the client waits five minutes before running logon scripts by default
  (the policy **Configure Logon Script Delay** is Not Configured). To run them immediately set it to Disabled, or
  to Enabled with 0 minutes; the maximum delay is 1,000 minutes. Path: Computer Configuration > Administrative
  Templates > System > Group Policy.
- Foreground processing can be asynchronous, so the desktop can appear before user policy finishes.

## Prefer alternatives
Drive maps, printers, shortcuts, registry and files are better done with Group Policy Preferences (item-level
targeting, logged, no script). Scripts are for what GPP cannot do.

## Troubleshoot
- `gpresult /h` shows which GPOs applied.
- Add logging inside the script (for example `Start-Transcript`) so you can see when it ran and under which account.

## Verify
- [ ] Script's own log shows it ran at the expected time under the expected account.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: the Configure Logon Script Delay policy (default behaviour of waiting five minutes on Windows 8.1, Disabled or 0 minutes to run immediately, 1,000 minute maximum, policy path), script processing during refresh with individual scripts running only at startup, shutdown, logon and logoff, and that foreground processing can be asynchronous. Removed as unconfirmed: the SYSTEM and user run-as table, the Machine Scripts Startup folder layout, the PowerShell Scripts tab and ordering option, the 600 second script time-out, slow-link skipping, events 5018 and 4018, and the execution policy advice.

Method: documentation only; no commands were run.
