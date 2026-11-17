---
id: computing-software.it-support-helpdesk.device-provisioning.pxe-boot-and-wds
name: pxe-boot-and-wds
category: computing-software
field: it-support-helpdesk
product: device-provisioning
tags: [it-support-helpdesk, device-provisioning, pxe-boot, wds, configmgr, dhcp, ip-helper, uefi, tftp, winpe-boot-images]
level: practitioner
status: draft
description: "Get PXE booting working: ConfigMgr PXE responder vs WDS, IP helpers over DHCP options, UEFI boot files, boot image distribution, SMSPXE.log and slow TFTP fixes."
sources:
  - "https://learn.microsoft.com/en-us/mem/configmgr/osd/deploy-use/use-pxe-to-deploy-windows-over-the-network"
  - "https://learn.microsoft.com/en-us/mem/configmgr/osd/plan-design/infrastructure-requirements-for-operating-system-deployment"
  - "https://learn.microsoft.com/en-us/troubleshoot/mem/configmgr/os-deployment/understand-pxe-boot"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# pxe-boot-and-wds

## Pieces
1. Client firmware does DHCP with PXE options.
2. A PXE server answers with the boot file and server (ConfigMgr distribution point with
   PXE enabled, optionally using the PXE responder without WDS).
3. TFTP downloads the boot file and boot image; WinPE starts the task sequence.

## Network: prefer IP helpers
- Configure the router/switch `ip helper-address` on each client VLAN to point at both the
  DHCP server and the PXE-enabled DP. This handles BIOS and UEFI correctly.
- DHCP options 66/67 hard-code one boot file and break mixed BIOS/UEFI; Microsoft
  recommends against them.
- UEFI boot file served by ConfigMgr: `smsboot\x64\wdsmgfw.efi`; BIOS: `smsboot\x64\wdsnbp.com`.

## ConfigMgr setup checklist
- DP properties: Enable PXE support, Allow this DP to respond to incoming PXE requests,
  Enable unknown computer support (for bare metal), optional PXE password.
- Boot image (x64) has "Deploy this boot image from the PXE-enabled distribution point"
  and is distributed to that DP.
- A task sequence is deployed to a collection the device is in (Unknown Computers for new
  devices), available to "media and PXE".

## Troubleshoot
| Symptom | Check |
|---|---|
| PXE-E53 / no boot filename | Helper or DHCP not reaching the DP; DP service down |
| Boots then "Abortpxe" / no TS | Device known but no deployment, or old record; delete the device record |
| TFTP very slow | Raise RamDisk TFTP block and window size on the DP (registry or DP settings) |
| Secure Boot rejects boot | Boot image/ADK too old for the current Secure Boot DB; update ADK and boot images |

Log: `SMSPXE.log` on the DP shows each request by MAC/SMBIOS GUID and the decision.

## Gotchas
- Spanning tree port-fast off on access ports makes PXE time out before the link is up.
- Laptops without NICs need approved USB-C/USB NIC adapters listed in the boot image.

## Verify
A new device PXE boots on the client VLAN, SMSPXE.log shows the offer, WinPE loads and
the task sequence wizard appears.
