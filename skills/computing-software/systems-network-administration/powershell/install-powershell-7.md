---
id: computing-software.systems-network-administration.powershell.install-powershell-7
name: install-powershell-7
category: computing-software
field: systems-network-administration
product: powershell
tags: [powershell, powershell-environment, pwsh, install-powershell-7, msi-deployment, winget, lts, microsoft-update, side-by-side]
level: practitioner
status: docs-checked
description: "Deploy and keep PowerShell 7 current on Windows servers side by side with 5.1: LTS vs stable, MSI switches, winget, Microsoft Update opt-in, remoting endpoint and verification."
sources:
  - https://learn.microsoft.com/en-us/powershell/scripting/install/installing-powershell-on-windows
  - https://learn.microsoft.com/en-us/powershell/scripting/install/powershell-support-lifecycle
  - https://learn.microsoft.com/en-us/powershell/scripting/install/microsoft-update-faq
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Install and update PowerShell 7 side by side

PowerShell 7 (`pwsh.exe`) installs side by side with Windows PowerShell 5.1 (`powershell.exe`), which stays part of the OS.
The MSI default folder is under `$Env:ProgramFiles\PowerShell\` in a versioned subfolder (`7`; previews use `7-preview`).

## Pick a release line
- **LTS**: an LTS release of PowerShell is built on an LTS release of .NET, and receives only critical security and
  servicing fixes. Use for servers.
- **Stable**: a release between LTS releases, supported for about six months after the next LTS release. Fine for admin workstations.
- Preview installs side by side with stable (`7-preview` folder). Keep it off servers.
Check the supported-versions table in the support lifecycle doc for current versions and end-of-support dates.

## Install options
```powershell
winget install --id Microsoft.PowerShell --source winget     # interactive/workstation; winget installs the MSIX package by default since 7.6
```
Silent MSI for deployment tools (ConfigMgr, Intune, GPO startup script):
```powershell
msiexec.exe /package PowerShell-7.x.y-win-x64.msi /quiet `
  ADD_EXPLORER_CONTEXT_MENU_OPENPOWERSHELL=1 ADD_FILE_CONTEXT_MENU_RUNPOWERSHELL=1 `
  ENABLE_PSREMOTING=1 REGISTER_MANIFEST=1 USE_MU=1 ENABLE_MU=1 ADD_PATH=1
```
| Property | Effect |
|---|---|
| `ENABLE_PSREMOTING=1` | enables PowerShell remoting for this version |
| `REGISTER_MANIFEST=1` | registers the Windows Event Logging manifest |
| `USE_MU=1 ENABLE_MU=1` | opt in to updates via Microsoft Update / WSUS |
| `ADD_PATH=1` | adds pwsh to PATH |
| `DISABLE_TELEMETRY=1` | sets `POWERSHELL_TELEMETRY_OPTOUT` |

The ZIP package needs no installer but you add shortcuts and PATH yourself: use it for portable tooling or a second side-by-side version, not as a fleet standard.

## Updates
- With `USE_MU=1`, updates come through Microsoft Update, WSUS, WUfB or Configuration Manager.
- Microsoft Update only upgrades within the same channel (LTS to LTS, stable to stable) and never moves an LTS install to a non-LTS release.

## Remoting into PowerShell 7
Remoting targets Windows PowerShell 5.1 unless you name a PowerShell 7 session configuration. Install with
`ENABLE_PSREMOTING=1` where you need remoting into 7, then use `Get-PSSessionConfiguration` on the target to find the
configuration name and pass it as `-ConfigurationName`.

## Scheduled tasks and scripts
Point tasks at the full path of `pwsh.exe` with `-NoProfile -File <SCRIPT_PATH>`.
Add a `#Requires` version statement to scripts that need 7.

## Verify
- [ ] `pwsh -v` reports the expected LTS version on every server (inventory via fan-out).
- [ ] A PowerShell 7 session configuration exists where remoting into 7 is needed.
- [ ] WSUS/WUfB reports PowerShell updates as applicable/installed.

## Checked
2026-11-01. Confirmed against the Windows install page, the support lifecycle page and the Microsoft Update FAQ: LTS and Stable
definitions, `7-preview` folder, MSI properties (`ENABLE_PSREMOTING`, `REGISTER_MANIFEST`, `USE_MU`, `ENABLE_MU`, `ADD_PATH`,
`DISABLE_TELEMETRY`), winget MSIX default from 7.6, MU channel rules. Removed the support-length figures, odd/even rule, the
`PowerShell.7` endpoint name and unconfirmed command forms.
Method: documentation only; no commands were run.
