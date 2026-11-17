---
id: computing-software.it-support-helpdesk.desktop-support.gpresult-and-gpupdate-for-policy-troubleshooting
name: gpresult-and-gpupdate-for-policy-troubleshooting
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, command-line-tools, gpresult-report, gpresult, gpupdate, rsop, group-policy, security-filtering, wmi-filter, loopback-processing, comptia-a-plus]
level: practitioner
status: docs-checked
description: "Find out why a Group Policy setting does or does not apply: gpupdate, gpresult /h reports, denied GPO reasons, security and WMI filtering, loopback, and GP event logs."
sources:
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult"
  - "https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpupdate"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/applying-group-policy-troubleshooting-guidance"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/cannot-apply-user-gpo-when-computer-objects-dont-have-read-permissions"
  - "https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/loopback-processing-of-group-policy"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# gpresult-and-gpupdate-for-policy-troubleshooting

Goal: answer "is the policy applied to this user or computer, and if not,
why?" from evidence.

## Refresh
```cmd
gpupdate /force                 :: reapply all settings
gpupdate /target:computer /force
```
`/logoff` logs off after the update (needed for extensions that process only
at sign-in, such as Folder Redirection and user software installation), and
`/boot` restarts if required. A PC that cannot reach a domain controller
cannot refresh policy.

## Report
```cmd
gpresult /r                                 :: summary (user and computer)
gpresult /scope computer /r
gpresult /h %TEMP%\gp.html /f               :: HTML report, /f overwrites
gpresult /user CORP\sam /h %TEMP%\gp-sam.html
```
`gpresult` needs an output option (`/r`, `/v`, `/z`, `/x` or `/h`). Without
`/scope` it reports on both user and computer. `/x` and `/h` cannot be used
with `/u`, `/p`, `/r`, `/v` or `/z`. For `/user`, write `<domain>\<user>`.

## Denied GPOs
The Group Policy Operational event log lists applied GPOs and a list of
**denied** GPOs with the reasons. Common causes:
- **Security filtering**: if Authenticated Users is removed from a GPO's
  security filtering, the **computer account still needs Read permission**
  on the GPO for user settings to apply. Grant Read to Authenticated Users
  (read only), Domain Computers, or the specific computers. Domain controllers
  are unaffected because Enterprise Domain Controllers has Read by default.
- **OU placement** and **loopback processing**: Group Policy applies according
  to where the user and computer objects sit; loopback is the feature that
  applies user settings by computer location (kiosks, shared PCs).

## Event logs
Event Viewer, Applications and Services Logs, Microsoft, Windows, GroupPolicy,
Operational (`Microsoft-Windows-GroupPolicy/Operational`).
- **1129**: processing failed for lack of network connectivity to a domain
  controller (check LDAP port 389 and name resolution).
- **1030**: processing failed; look at the Details tab for the error code and
  check DNS and connectivity to a DC.
- **1058**: Windows could not read a file from a domain controller (name
  resolution, DFS or SYSVOL replication latency, or the DFS client disabled).

## Gotchas
- Run an elevated prompt for computer settings.
- Time skew above five minutes between the PC and the DC can make
  authentication fail; resync with `w32tm /resync`.

## Verify
`gpresult` lists the GPO under applied GPOs, and the behaviour matches after
any required sign-out or reboot.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn gpresult and gpupdate command pages, and Microsoft Support Group Policy troubleshooting, loopback and computer-Read-permission articles (dated 2025-2026). Confirmed: gpupdate /force, /target, /logoff, /boot; gpresult syntax, /scope default, /h and /f behaviour and /x,/h exclusions; Operational log contents; the computer Read-permission requirement and its three remedies; events 1129, 1030 and 1058 descriptions; five-minute time skew. Removed: 90 plus or minus 30 minute interval, MS16-072 label, the WMI/Empty/Disabled reason table, MDM-wins-over-GP and GPP apply-once notes, exam reference.

Method: documentation only; no commands were run.
