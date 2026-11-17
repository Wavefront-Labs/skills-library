---
id: computing-software.systems-network-administration.windows-server.group-policy-client-processing-and-slow-link
name: group-policy-client-processing-and-slow-link
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, group-policy, slow-link-detection, gpupdate, background-refresh, loopback-processing]
level: advanced
status: docs-checked
description: "Control how clients apply Group Policy: foreground vs background refresh, gpupdate options, synchronous processing, slow link detection and loopback mode."
sources:
  - https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/group-policy/group-policy-processing
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpupdate
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/gpresult
  - https://learn.microsoft.com/en-us/powershell/module/grouppolicy/invoke-gpupdate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Policy client processing and slow links

## When policy applies
- **Foreground**: at boot (computer) and logon (user). Foreground processing can be synchronous or asynchronous; some
  client-side extensions only process at startup or logon (hence `gpupdate /boot` and `/logoff`). Policy processing
  must finish within 60 minutes (not configurable).
- **Background**: every 90 minutes with a random offset of up to 30 minutes; domain controllers check every 5 minutes.
  Background refresh applies settings asynchronously.
- Scripts are processed during refresh but individual scripts run only at startup, shutdown, logon and logoff.

## gpupdate
```cmd
gpupdate /target:computer /force        REM reapply all, not only changed GPOs
gpupdate /force /boot /logoff           REM reboot/logoff if a foreground-only extension needs it
gpupdate /sync                          REM next foreground processing is synchronous
```
Remote: `Invoke-GPUpdate -Computer SRV01 -RandomDelayInMinutes 0 -Force` (needs the firewall rules
"Remote Scheduled Tasks Management (RPC)" and "(RPC-ERMAP)").

## Slow link detection
On a slow network connection (for example dial-up) the response varies among policies: each policy can specify how it
reacts to a slow link. Check the specific extension's slow-link setting rather than assuming a threshold.
- Check what applied: `gpresult /h r.html` (or `/r`, `/v`); `/scope computer|user` limits the report.

## Loopback
"Configure user Group Policy loopback processing mode": **Merge** (user GPOs + computer-OU user settings,
computer wins) or **Replace** (only the user settings of GPOs that apply to the computer). Use for RDS hosts and kiosks.

## Verify
- [ ] `gpresult /r` lists the expected GPOs after `gpupdate /force`.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed: foreground and background processing, the 90 minute refresh with up to 30 minutes random offset, the 5 minute domain controller check, the 60 minute processing time-out, script execution timing, loopback Merge and Replace behaviour, gpupdate switches (/target, /force, /wait, /logoff, /boot, /sync), gpresult /r /v /h /scope, and Invoke-GPUpdate parameters with the two Remote Scheduled Tasks Management firewall rules. Removed as unconfirmed: the 500 kbps slow-link default, NLA wording, the slow-link policy name and its zero value, the list of extensions skipped on slow links, event 5314, the claim that fast logon optimization is default behaviour, and the Always wait for the network setting.

Method: documentation only; no commands were run.
