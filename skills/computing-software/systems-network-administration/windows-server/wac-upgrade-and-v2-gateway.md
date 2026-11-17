---
id: computing-software.systems-network-administration.windows-server.wac-upgrade-and-v2-gateway
name: wac-upgrade-and-v2-gateway
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac-upgrade, wac-v2, modernized-gateway, migration]
level: practitioner
status: docs-checked
description: "Upgrade Windows Admin Center safely, including moving to the modernized v2 gateway: what changes (port, service, extensions), backup, and rollback."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/support/release-history
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/support/known-issues
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/deploy/install
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/configure/using-extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrade Windows Admin Center (and the v2 gateway)

## Before upgrading
- Export connections with `Export-WACConnection` from the ConnectionTools module (path and syntax in the connections skill).
- Note installed extensions and versions (Settings > Extensions) and the TLS certificate thumbprint and port.
- Snapshot the gateway VM.

## In-place upgrade within a generation
Run the new installer on the gateway and choose the TLS certificate (the pre-installed one, by thumbprint). Silent install options
are `/Silent`, `/VerySilent`, `/HTTPSPortNumber=<port>` and `/CertificateThumbprint=<thumbprint>`. Check extensions afterwards.

## Moving to the modernized gateway (v2, 2410+)
- Version 2410 moved the backend from .NET 4.6.2 to .NET 8 (release history); the installer is `WindowsAdminCenter.exe`.
- Known issue: when upgrading from 2311 to 2410 the existing certificate may not be set in the new installation, especially with
  international or special characters; re-apply it as in the certificate update article.
- A high-availability deployment on 2311 or older cannot be upgraded directly to 2410+; uninstall and reinstall (see the HA skill).
- Gateway plug-in extensions are most affected: .NET Framework 4.6.2 components do not run on .NET 8 and the plug-in model changed.
  Some extensions listed in known issues do not work on 2410 even with a feed added. Check vendor extensions first.
- PowerShell: the connections module uses `Export-WACConnection` / `Import-WACConnection`; the configuration module has `Set-WACCertificateSubjectName`; update scripts.

## Rollback
Restore the VM snapshot. If an install of a newer build over an older modernized build fails, the docs suggest uninstalling and reinstalling.

## Verify
- [ ] Version shown in the gateway settings; connections and extensions present; a sample server opens with the same
      credentials and delegation as before.

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (troubleshooting ms.date 2025-06-24; Azure VM and Arc pages current in repo), Windows Admin Center 2410+.
Confirmed from support/release-history (2410 .NET 8 backend), support/known-issues (2311 to 2410 certificate issue, extensions not working on 2410), configure/using-extensions (gateway plug-in changes),
deploy/high-availability (no direct HA upgrade to 2410+), deploy/install (installer options), includes/ps-connections and support/troubleshooting (reinstall advice).
Removed the msiexec property line, the claims that settings and RBAC migrate automatically and that incompatible extensions are disabled, and the Get-WACConnection cmdlet name, which the pages do not state.
Method: documentation only; no commands were run.
