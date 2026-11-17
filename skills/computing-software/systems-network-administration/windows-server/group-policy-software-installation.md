---
id: computing-software.systems-network-administration.windows-server.group-policy-software-installation
name: group-policy-software-installation
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, gp-advanced-settings, gpo-software-installation, msi, assign-publish, group-policy]
level: practitioner
status: docs-checked
description: "Deploy MSI packages with Group Policy Software Installation: assign vs publish, distribution share permissions, upgrades, transforms and when to move to Intune or ConfigMgr."
sources:
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/use-group-policy-to-install-software
  - https://learn.microsoft.com/en-us/troubleshoot/windows-server/group-policy/troubleshoot-software-installations-debug-logging
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Group Policy Software Installation

Windows Installer (.msi) packages deployed through Group Policy software installation.

## Distribution point
- Create a shared folder and set share permissions that allow access to the package; copy the `.msi` there (for an
  installer use the administrative installation, `setup.exe /a`, to copy the files).
- The package path is stored in the GPO, so keep it stable.

## Assign vs publish
| | Computer config | User config |
|---|---|---|
| Assigned | installed when the computer starts, available to all users | installed at logon; installation completes when the user first runs it |
| Published | not available | listed for installation from the Control Panel program list |
Computer assignment is the reliable choice.

## Create
GPMC > GPO > Computer Configuration > Policies > Software Settings > Software installation > New > Package >
UNC path to the `.msi` > Assigned.

## Upgrades and removal
- Remove: All Tasks > Remove > **Immediately uninstall the software from users and computers** or **Allow users to
  continue to use the software but prevent new installations**.

## Troubleshoot
- Computer-assigned packages install when the computer starts, so a restart is needed.
- Application management debug log: create the DWORD `AppMgmtDebugLevel` = `4b` under
  `HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\Diagnostics` on the target; `Appmgmt.log` is written to
  `%SystemRoot%\Debug\UserMode`. Microsoft notes this debug logging does not work on Windows 8 or Windows Server 2012; delete the value
  afterwards.

## Verify
- [ ] The application is installed on a pilot machine after restart.

## Checked

Checked 2026-10-26 against learn.microsoft.com / MicrosoftDocs/windowsserverdocs, windows-powershell-docs and SupportArticles-docs main branches, last commits 2026-10-23. Confirmed in the Group Policy software installation article: assigning versus publishing semantics, creating a distribution point and administrative installation, removal options, and the AppMgmtDebugLevel value 4b with Appmgmt.log location and the Windows 8 and Server 2012 limitation. Removed as unconfirmed: share and NTFS permissions for Domain Computers, DFS advice, the Install at logon and transform details, the upgrade options, foreground-only and slow-link behaviour, events 101-108, 1005, 302 and 308, the Windows Installer verbose logging value, and the Intune and ConfigMgr guidance. Note the source article is written for older Windows versions.

Method: documentation only; no commands were run.
