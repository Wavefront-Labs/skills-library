---
id: computing-software.systems-network-administration.windows-server.windows-deployment-services-pxe
name: windows-deployment-services-pxe
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, server-install, pxe-boot, wds, windows-deployment-services, boot-image]
level: practitioner
status: docs-checked
description: "Deploy Windows Server over the network with Windows Deployment Services: install the WDS role, initialize with wdsutil, add images and PXE-boot a test VM."
sources:
  - https://learn.microsoft.com/en-us/windows/deployment/windows-deployment-scenarios-and-tools
  - https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/wdsutil
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network deployment with Windows Deployment Services

WDS answers PXE requests and serves boot images (WinPE) and install images (WIM). Often used under MDT or
ConfigMgr; still handy alone for labs and small sites.

## Install and initialize
```powershell
Install-WindowsFeature WDS-Deployment -IncludeManagementTools
```
Then initialize the server with `wdsutil /initialize-server` (see the wdsutil page for its options) or the WDS console,
and add boot and install images.

## PXE across subnets
The WDS server must be able to communicate with DHCP (and optionally AD DS). Check the WDS documentation for DHCP
options and IP helper (relay) configuration before relying on either.

## Troubleshoot
- Log: Event Viewer > Applications and Services Logs > Microsoft > Windows > Deployment-Services-Diagnostics.

## Verify
- [ ] A test VM (Gen 2) PXE-boots into WinPE and finds the install images.

## Checked

2026-10-28. Confirmed against: Install-WindowsFeature WDS-Deployment, the wdsutil command list (initialize-server) and the Deployment-Services-Diagnostics log location (BitLocker Network Unlock page). Removed (not confirmable from the cited pages): wdsutil flags (reminst, answerclients, add-image, tftpblocksize), the boot.wim support statement, DHCP options 66/67 and vendor-class file names, UEFI/Secure Boot notes, PXE error codes.

Method: documentation only; no commands were run.
