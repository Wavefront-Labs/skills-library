---
id: computing-software.systems-network-administration.windows-server.sysprep-golden-images
name: sysprep-golden-images
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server-installation, sysprep-generalize, sysprep, golden-image, unattended-install]
level: practitioner
status: docs-checked
description: "Build Windows Server golden images with sysprep /generalize: what to install first, unattend specialize settings, limits on rearm and common sysprep failures."
sources:
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep--generalize--a-windows-installation
  - https://learn.microsoft.com/en-us/windows-hardware/manufacture/desktop/sysprep-command-line-options
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sysprep and golden images

Cloning a server without generalizing it copies machine-specific identity; generalize with Sysprep before capture.

## Build order
1. Install the OS from patched media, apply all updates, reboot until none pending.
2. Install only agents that support imaging; some need a "prepare for image" step (check each vendor). Leave domain join
   to deployment time.
3. Configure defaults; keep identity-bound roles (AD DS, AD CS, DHCP authorisation) out of images.
4. Clean up with `dism /Online /Cleanup-Image /StartComponentCleanup`, clear logs and temp.

## Generalize
```cmd
%WINDIR%\System32\Sysprep\sysprep.exe /generalize /oobe /shutdown /unattend:<UNATTEND_XML>
```
- `/mode:vm` when the generalized VHD will be deployed only as a VHD on the same VM or hypervisor.
- Capture after shutdown (for example with DISM image capture) or use the VHDX as a template.

## Unattend specialize pass
Set computer name, time zone and local admin password in the answer file (use a LAPS policy after join rather than a
shared image password); look up each setting in the Windows Unattended Setup reference.

## Common failures
| Symptom | Fix |
|---|---|
| Sysprep fails validation | Check the logs in `%WINDIR%\System32\Sysprep\Panther`; Learn documents an Appx package installed for one user but not provisioned for all users as a cause |
| Pending reboot | finish updates and reboot first |

## Verify
- [ ] Two deployed machines have distinct computer names and no shared identity left over from the image.
- [ ] First boot completes OOBE unattended and joins the domain via the deployment tool.

## Checked
2026-10-28. Confirmed on the Learn Sysprep generalize and command-line pages: `/generalize /oobe /shutdown /unattend` syntax,
`/mode:vm` meaning, Panther log folder and the per-user Appx failure, StartComponentCleanup in DISM. Removed as
unconfirmed: the SID-duplication consequences, the rearm-count row (Learn only says SkipRearm applied to older
releases), CopyProfile and RegisteredOrganization advice, named agent offboarding steps, New-WindowsImage.
Method: documentation only; no commands were run.
