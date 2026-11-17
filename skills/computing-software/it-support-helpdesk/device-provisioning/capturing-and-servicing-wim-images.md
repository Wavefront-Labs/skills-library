---
id: computing-software.it-support-helpdesk.device-provisioning.capturing-and-servicing-wim-images
name: capturing-and-servicing-wim-images
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, wim-image, dism, sysprep, image-servicing, offline-servicing, imaging]
level: practitioner
status: draft
description: "Capture a reference Windows image with Sysprep and DISM, service WIMs offline (updates, drivers, cleanup), export to shrink, and fix the classic Sysprep failures."
sources:
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/capture-and-apply-windows-using-a-single-wim"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/mount-and-modify-a-windows-image-using-dism"
  - "https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep--generalize--a-windows-installation"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# capturing-and-servicing-wim-images

## Decide first
Most estates no longer need a custom fat image: OEM or stock media plus Autopilot and
Intune apps is easier to keep current. Capture a reference image only when offline
builds, labs, or heavy app stacks demand it, and keep it thin.

## Capture
1. Build the reference in a VM (no OEM drivers), patched, apps only if they cannot be
   deployed later. Do it in Audit mode (`Ctrl`+`Shift`+`F3` at OOBE).
2. Generalize: `%WINDIR%\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown`.
3. Boot WinPE and capture (drive letters in WinPE vary; check with `diskpart` > `list vol`):
```cmd
DISM /Capture-Image /ImageFile:<IMAGE_DIR>\ref.wim /CaptureDir:<OS_DRIVE>\ /Name:"Win11-24H2-Ref" /Compress:max /CheckIntegrity
```

## Service offline
```cmd
DISM /Get-WimInfo /WimFile:<IMAGE_DIR>\install.wim
DISM /Mount-Image /ImageFile:<IMAGE_DIR>\install.wim /Index:1 /MountDir:<MOUNT_DIR>
DISM /Image:<MOUNT_DIR> /Add-Package /PackagePath:<UPDATES>\windows11.0-kbXXXXXXX-x64.msu
DISM /Image:<MOUNT_DIR> /Add-Driver /Driver:<DRIVERS> /Recurse
DISM /Image:<MOUNT_DIR> /Cleanup-Image /StartComponentCleanup /ResetBase
DISM /Unmount-Image /MountDir:<MOUNT_DIR> /Commit
DISM /Export-Image /SourceImageFile:<IMAGE_DIR>\install.wim /SourceIndex:1 /DestinationImageFile:<IMAGE_DIR>\install-new.wim
```
- Apply the servicing stack update before the cumulative update (newer combined packages
  handle this themselves).
- Export after servicing: deleted payloads stay in the WIM until exported.
- `/ResetBase` makes installed updates permanent; do it only on images you will not roll
  back.

## Sysprep failures
- Check `%WINDIR%\System32\Sysprep\Panther\setupact.log` and `setuperr.log`.
- "Package ... was installed for a user, but not provisioned for all users": a Store app
  updated for the build user. Remove it with `Remove-AppxPackage` for that user, or keep
  the reference offline so Store updates do not run.
- Rearm limit or BitLocker on: decrypt and use a fresh VM.

## Gotchas
- Leftover mounted images: `DISM /Get-MountedWimInfo` then `/Unmount-Image /Discard` and
  `DISM /Cleanup-Wim`.
- Never capture with management agents installed (RMM, ConfigMgr client IDs, AV agents
  without their image-prep step).

## Verify
`DISM /Get-WimInfo` shows the new index and build, a test deployment boots to OOBE with
the expected patch level (`winver`), and no orphaned mounts remain.
