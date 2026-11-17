---
id: computing-software.systems-network-administration.windows-server.safe-mode-and-boot-options
name: safe-mode-and-boot-options
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, boot-troubleshooting, winre, safe-mode, bcdedit-safeboot, last-known-good, boot-logging, disable-driver-signature, ntbtlog]
level: practitioner
status: gated
description: "Use safe mode and advanced boot options on servers: bcdedit safeboot variants, boot logging, disabling a bad driver or service offline, and getting out of safe mode."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/drivers/devtest/bcdedit--set
licence: Apache-2.0
version: 5
updated: 2026-11-17
---

# Safe mode and boot configuration options

Set boot options with bcdedit (from a running OS or WinRE); do not rely on F8.

## Enter safe mode
```
bcdedit /set {default} safeboot minimal          # safe mode
bcdedit /set {default} safeboot network          # with networking

bcdedit /set {default} safebootalternateshell yes   # with command prompt (plus minimal)
shutdown /r /t 0
```
**Remember to leave**: `bcdedit /deletevalue {default} safeboot`, otherwise the server
reboots into safe mode forever. `bcdedit /set {default} bootmenupolicy legacy` selects the legacy boot menu
(see the bcdedit /set reference for which Windows versions default to which menu).

## Boot logging and other options
```
bcdedit /set {default} bootlog yes        # Ntbtlog.txt in %WINDIR%: loaded and unloaded drivers
bcdedit /set {default} sos yes            # show drivers while loading
bcdedit /set {default} nointegritychecks yes   # test only; cannot be set when Secure Boot is enabled
```
WinRE > Startup Settings offers a similar one-boot menu.

## Disable a bad driver/service offline (WinRE)
```
reg load HKLM\OFFSYS <WinVol>:\Windows\System32\config\SYSTEM
reg query "HKLM\OFFSYS\ControlSet001\Services\baddrv" /v Start
reg add "HKLM\OFFSYS\ControlSet001\Services\baddrv" /v Start /t REG_DWORD /d 4 /f
reg unload HKLM\OFFSYS
```
Start 4 means disabled (see Microsoft's Services registry documentation). Also check `UpperFilters`/`LowerFilters` on
device classes when a filter driver (AV, backup) blocks boot.

## Verify
- [ ] Safeboot value removed; server boots normally; offending driver/service identified in Ntbtlog.txt.

## Checked
2026-10-28. Confirmed on the Learn bcdedit /set page: `safebootalternateshell`, `bootlog` and Ntbtlog.txt, `sos`,
`nointegritychecks` with the Secure Boot limit, `bootmenupolicy` Legacy/Standard, `/deletevalue`. Removed as
unconfirmed: `safeboot dsrepair`, `displaybootmenu`, the Last Known Good paragraph, the exact Startup Settings entries.
Left as general practice, not from this page: the offline-registry Start value 4 and `safeboot minimal/network`
(gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
