---
id: computing-software.systems-network-administration.windows-server.offline-image-servicing-with-dism
name: offline-image-servicing-with-dism
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server-installation, dism-offline-servicing, add-windowsdriver, wim, install-media]
level: advanced
status: gated
description: "Service install.wim offline with DISM: mount the right index, inject drivers and cumulative updates, enable features, clean up and recapture smaller media."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/mount-and-modify-a-windows-image-using-dism
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/add-and-remove-drivers-to-an-offline-windows-image
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Offline image servicing with DISM

Patching the image means new servers come up current, with storage and NIC drivers that setup needs.

## Pick the index
```powershell
Get-WindowsImage -ImagePath <MEDIA>\sources\install.wim
```
Use `Get-WindowsImage` (or `dism /Get-ImageInfo`) to list the indexes and pick one by name.

## Mount, service, commit
```powershell
New-Item -ItemType Directory <MOUNT_DIR>
Mount-WindowsImage -ImagePath <WORK>\install.wim -Index 2 -Path <MOUNT_DIR>
# Drivers (folder of .inf drivers, recursive)
Add-WindowsDriver -Path <MOUNT_DIR> -Driver <DRIVERS_DIR> -Recurse
# Add the latest cumulative update
Add-WindowsPackage -Path <MOUNT_DIR> -PackagePath <UPDATES>\windows-server-lcu.msu
# Clean superseded components to shrink the image
dism /Image:<MOUNT_DIR> /Cleanup-Image /StartComponentCleanup /ResetBase
Dismount-WindowsImage -Path <MOUNT_DIR> -Save
```

## Boot images too
Add storage/NIC drivers to `boot.wim` (Learn's Windows PE page shows this with the same DISM `/Add-Driver` approach) so
setup sees the disks.

## Shrink
Learn's example follows `/StartComponentCleanup /ResetBase` with unmount `/Commit` and `Dism /Export-Image` to a new
.wim to reduce the file size.

## Gotchas
- Always commit or discard changes when unmounting (Learn: use `/commit` to save changes to the mounted image).
- Use a DISM version matching or newer than the image's OS.
- `/ResetBase` removes the ability to uninstall superseded components; check Learn's note before using it.

## Verify
- [ ] The cumulative update appears in the mounted image's package list before dismount.
- [ ] A test install reports the expected build (`winver`) and has drivers loaded.

## Checked
2026-10-28. Confirmed on the Learn mount/modify and offline-driver pages: `DISM /Mount-Image`, `/Add-Driver /Driver:<folder> /Recurse`,
`/Unmount-Image /Commit`, `/cleanup-image /StartComponentCleanup /ResetBase`, `/Export-Image`, drivers added to boot.wim.
Removed as unconfirmed: NetFx3 sxs step, SWM split command, winre.wim/Safe OS update line, servicing-stack bundling
remark, Clear-WindowsCorruptMountPoint. The PowerShell cmdlet spellings of the DISM operations (Mount-WindowsImage,
Add-WindowsDriver, Add-WindowsPackage, Dismount-WindowsImage) were not checked against their module pages
(gated: unconfirmed, source is paywalled or blocked).
Method: documentation only; no commands were run.
