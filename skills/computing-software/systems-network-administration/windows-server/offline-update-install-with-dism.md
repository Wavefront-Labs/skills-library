---
id: computing-software.systems-network-administration.windows-server.offline-update-install-with-dism
name: offline-update-install-with-dism
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-updates, servicing, dism-add-package, msu-install, wusa, add-windowspackage, servicing-stack-update, checkpoint-cumulative-update, image-servicing, offline-patching]
level: practitioner
status: docs-checked
description: "Install MSU/CAB updates without Windows Update using DISM /Add-Package online and into mounted WIM images, including checkpoint cumulative updates."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-or-remove-packages-offline-using-dism
  - https://learn.microsoft.com/en-us/windows/deployment/update/catalog-checkpoint-cumulative-updates
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline update install (MSU/CAB with DISM)

Use for isolated servers, golden images, or when Windows Update/WSUS is broken.

## Get the packages
Download the `.msu` or `.cab` files from the Microsoft Update Catalog. Windows Server 2025 uses checkpoint cumulative
updates: the latest cumulative update may need an earlier cumulative update installed first. The checkpoint page lists
the packages and the install order (install each MSU in order with DISM or Windows Update Standalone Installer).

## Online (running server)
```cmd
DISM /Online /Add-Package /PackagePath:<PKG_DIR>\
```
`/PackagePath` can point to a `.cab` file or a folder.

## Offline image (WIM) servicing
```cmd
DISM /Mount-Image /ImageFile:<MEDIA>\sources\install.wim /Index:2 /MountDir:<MOUNT_DIR>
DISM /Image:<MOUNT_DIR> /Add-Package /PackagePath:<PKG_DIR>\
DISM /Image:<MOUNT_DIR> /Cleanup-Image /StartComponentCleanup /ResetBase
DISM /Unmount-Image /MountDir:<MOUNT_DIR> /Commit
```
Monthly cumulative updates apply to the main OS (`install.wim`) and WinPE (`boot.wim`) but not to WinRE (`winre.wim`).

## Gotchas
- After `/ResetBase`, installed Windows updates can't be uninstalled.

## Verify
- [ ] `DISM /Online /Get-Packages /Format:Table` lists the new package.

## Checked

2026-10-28. Confirmed against: Add or remove packages offline using DISM (Mount-Image, Add-Package, Unmount-Image /Commit, folder PackagePath), DISM operating system package servicing options (Get-Packages /Format:Table, /StartComponentCleanup /ResetBase) and the checkpoint cumulative updates page (Server 2025). Removed (not confirmable from the cited pages): wusa command, Add-WindowsPackage, catalog search strings, SSU claims, error codes 0x800f081f/0x800f0922, UBR and Get-HotFix checks, Safe OS dynamic update advice.

Method: documentation only; no commands were run.
