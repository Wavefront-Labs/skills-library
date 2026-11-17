---
id: computing-software.it-support-helpdesk.desktop-support.supporting-wsl-on-managed-pcs
name: supporting-wsl-on-managed-pcs
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, virtualization, client-virtualization, wsl, wsl2, wsl-install, wslconfig, wsl-networking, mirrored-networking, vpn-dns, wsl-export]
level: practitioner
status: docs-checked
description: "Install and support WSL for developers on managed Windows: wsl --install, version and distro management, .wslconfig limits, VPN/DNS and proxy fixes, backups and policy controls."
sources:
  - "https://learn.microsoft.com/en-us/windows/wsl/install"
  - "https://learn.microsoft.com/en-us/windows/wsl/wsl-config"
  - "https://learn.microsoft.com/en-us/windows/wsl/networking"
  - "https://learn.microsoft.com/en-us/windows/wsl/basic-commands"
  - "https://learn.microsoft.com/en-us/windows/wsl/enterprise"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# supporting-wsl-on-managed-pcs

Goal: developers get a working Linux environment on Windows that survives
the corporate VPN, proxy and security tooling.

## Install and manage
```powershell
wsl --install                    # run PowerShell as administrator, then restart
wsl --install -d Debian
wsl --list --online              # available distributions
wsl --list --verbose             # distros, state, version 1/2
wsl --update
wsl --shutdown                   # stop all distros (applies .wslconfig changes)
wsl --set-default-version 2
```
`wsl --install` needs Windows 10 version 2004 (build 19041) or later, or
Windows 11, and only works if WSL is not installed at all. If it prints the
help text, use `wsl --list --online` then `wsl --install -d <DistroName>`; if
it hangs at 0.0%, try `wsl --install --web-download -d <DistroName>`.
Run a distro as another user with `wsl --user <Username>`.

## Resource limits and networking: %USERPROFILE%\.wslconfig
```ini
[wsl2]
memory=8GB
processors=4
swap=4GB
networkingMode=mirrored     # requires Windows 11 22H2 or later
dnsTunneling=true
autoProxy=true              # use the Windows HTTP proxy information
```
Run `wsl --shutdown` to apply. Microsoft describes mirrored networking as
improving compatibility with VPNs, DNS tunneling as answering DNS from inside
WSL through a virtualization feature (aimed at VPN and complex network
set-ups), and autoProxy as making WSL use the Windows HTTP proxy. The bridged
networking mode is deprecated since WSL 2.4.5.

## VPN / DNS / proxy
- In the default NAT mode, VPN DNS may not reach WSL. Try
  `networkingMode=mirrored` plus `dnsTunneling=true`.
- Alternative: in `/etc/wsl.conf` set `[network]` `generateResolvConf=false`
  and write your own `/etc/resolv.conf`.
- For a proxy inside the distro use `autoProxy=true` or proxy environment
  variables.

## Files and backup
- Windows can browse Linux files at `\\wsl$`; Microsoft recommends keeping
  project files in the Linux file system for performance.
- Back up or migrate with `wsl --export <Distro> <FileName>` and
  `wsl --import <Distro> <InstallLocation> <FileName>`.

## Policy and security
Microsoft's enterprise guidance covers managing WSL with Intune or Group
Policy (including access to WSL and its key security settings) and the
Microsoft Defender for Endpoint plug-in for WSL, which lets security teams
monitor security events in running distributions.

## Verify
`wsl -l -v` shows the distro on version 2 and Running, and network access
from inside works on and off the VPN.


## Checked

Date 2026-10-27. Documentation release: Microsoft Learn WSL install, basic commands, wsl-config, networking, file systems and enterprise pages, as published October 2026. Confirmed: wsl --install requirements and fallbacks, --list --online and --verbose, --set-default-version, --shutdown, --user, --export/--import, .wslconfig keys memory, processors, swap, networkingMode (mirrored needs Windows 11 22H2+), dnsTunneling and autoProxy, bridged deprecation, generateResolvConf, the wsl$ share, Intune/Group Policy and MDE plug-in guidance. Removed: ext4.vhdx location and OneDrive note, Linux password reset steps, CA import commands, 'wsl --update' package-type remark.

Method: documentation only; no commands were run.
