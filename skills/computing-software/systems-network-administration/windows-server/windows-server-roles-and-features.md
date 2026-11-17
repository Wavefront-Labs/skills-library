---
id: computing-software.systems-network-administration.windows-server.windows-server-roles-and-features
name: windows-server-roles-and-features
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, server-manager, roles, features, install-windowsfeature, get-windowsfeature, uninstall-windowsfeature, servermanager-module, features-on-demand, server-core, desktop-experience, sconfig, windows-admin-center, rsat, dism, source-wim, sxs, includemanagementtools, configurationfilepath, remove-payload, ad-ds, dhcp, dns, iis, hyper-v, file-services, failover-clustering, windows-server-2022, windows-server-2025]
level: practitioner
status: docs-checked
description: "Install Windows Server roles and features with Install-WindowsFeature: management tools, wim: sources, exported configuration files and Server Core with sconfig."
sources:
  - https://learn.microsoft.com/en-us/powershell/module/servermanager/install-windowsfeature
  - https://learn.microsoft.com/en-us/windows-server/administration/server-core/what-is-server-core
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/configure-a-windows-repair-source
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Server roles and features — repeatable role builds, minimal footprint

**Goal:** add exactly the roles a server needs, from the command line, reproducibly,
including on Server Core and offline machines — and know what each choice costs.

## 1. Pick the installation option first
Server Core has no desktop shell; configure it with the SConfig tool or PowerShell (see the Server Core overview).

## 2. Discover and install
```powershell
Get-WindowsFeature | Where-Object Installed            # what's on the box
Get-WindowsFeature *dhcp*, *dns*                        # find exact Names
Install-WindowsFeature -Name DHCP -IncludeManagementTools -WhatIf
Install-WindowsFeature -Name DHCP -IncludeManagementTools
```
- `-IncludeManagementTools` installs the management tools with the role; add it explicitly.
- `-IncludeAllSubFeature` installs every sub-feature under a role, usually more than you want; name sub-features instead.
- `-WhatIf` previews the change; `-Restart` restarts the server if needed, so use it only in a maintenance window.
- Remote: `Install-WindowsFeature -Name X -ComputerName <SERVER>`, or for many servers use
  `Invoke-Command` (see
  `computing-software.systems-network-administration.powershell.pipeline-scripting-and-remoting`).

## 3. Repeatable builds
Configure one server in the GUI, then on the Confirm installation selections page choose *Export configuration settings*
to an XML, and replay it:
```powershell
Install-WindowsFeature -ConfigurationFilePath '<DIR>\role-web.xml' -ComputerName <SERVER>
```
Better still, keep the feature list in a script or DSC configuration
(`computing-software.systems-network-administration.powershell.dsc-and-configuration-management`)
so the build is reviewed and versioned.


## 4. Missing source files
If the payload is not available locally, pass `-Source` with a path or a WIM index using the `wim:` prefix:
```powershell
Install-WindowsFeature X -Source wim:<MEDIA>\sources\install.wim:2
```

## Verify
- [ ] `Get-WindowsFeature <Name>` shows `Installed` and management tools are present.
- [ ] Pending reboot handled.
- [ ] Post-install configuration done.
- [ ] The role list is captured in an XML, script or DSC config, not only in someone's memory.
- [ ] Unneeded roles/features are absent.

## Checked

2026-10-28. Confirmed against: Install-WindowsFeature reference (Name, IncludeManagementTools, IncludeAllSubFeature, Restart, WhatIf, Source, ComputerName, ConfigurationFilePath, Export configuration settings example), Server Core overview (SConfig, PowerShell administration) and the repair-source page (wim: prefix with image index). Removed (not confirmable from the cited pages): Server Core default/recommended and no-conversion claims, result object fields, AD DS and DHCP post-install commands, error 0x800f081f, Features on Demand, Uninstall-WindowsFeature -Remove, 2025 in-place upgrade note.

Method: documentation only; no commands were run.
