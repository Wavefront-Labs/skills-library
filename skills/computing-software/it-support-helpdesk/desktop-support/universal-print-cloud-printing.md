---
id: computing-software.it-support-helpdesk.desktop-support.universal-print-cloud-printing
name: universal-print-cloud-printing
category: computing-software
field: it-support-helpdesk
product: desktop-support
tags: [it-support-helpdesk, desktop-support, printer, printing, universal-print, cloud-printing, universal-print-connector, intune-printer-provisioning, serverless-printing, entra-id]
level: practitioner
status: docs-checked
description: "Support Microsoft Universal Print: native vs connector printers, how Intune provisions printers through the CSP, version limits and shared-device caveats."
sources:
  - "https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-whatis"
  - "https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-connector-overview"
  - "https://learn.microsoft.com/en-us/universal-print/fundamentals/universal-print-intune-tool"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# universal-print-cloud-printing

Goal: Entra-joined laptops print anywhere without a VPN or on-prem print server.

## Components
- **Universal Print ready printers** talk to the service directly; their firmware supports the Universal Print protocols and they need no connector.
- **Universal Print connector** is a bridge for printers that do not support those protocols. Installed on a Windows machine (client or server), it connects the printers installed on that machine. Its three jobs: let the admin register printers, report job and printer status, and fetch jobs from Universal Print and deliver them to the target printer. It passes jobs to the Windows print spooler; usually without storing the file, but sometimes it stores it temporarily, and in corner cases the deletion fails and the admin must delete the file by hand. Some Microsoft partners offer connector appliances.
- The service is built on IPP and Mopria standards, needs no print drivers, uses Microsoft Entra ID for identity, and is managed in the Azure portal. Print Support Apps (PSAs) let printer makers expose advanced functionality.

## Deploy to clients with Intune
Intune is the supported way to deploy Universal Print printers on managed Windows devices, through the Settings Catalog Universal Print configuration.
- Chain: Intune distributes the policy over the MDM channel, the Windows MDM client passes it to the Universal Print CSP, and the CSP runs `UPPrinterInstaller.exe` to add the printer. When a printer does not appear, work down the chain: policy assigned, device synced, CSP received the settings, installer failed.
- The CSP is available on Windows 11 and on Windows 10 with the July 2022 cumulative update (KB5015807) or later. Microsoft notes the Windows 10 path is supported only for devices with Extended Security Updates or being upgraded to Windows 11.
- Intune does not yet offer an uninstall option; users can remove printers by hand.

## Shared devices and upgrades
- Designed for one user per device, and for Azure Virtual Desktop where each session is a single-user device. Non-AVD shared Windows devices are not officially supported: expect silent install failures where Conditional Access requires MFA (password sign-in does not satisfy the MFA claim), and delayed or partial installs because Intune sync can take hours. Microsoft suggests Azure Virtual Desktop for shared use.
- Printers installed on Windows 10 are visible to all users of the device; on Windows 11 they are visible only to the installing user. After an upgrade, Windows 10 queues stay visible to everyone, and uninstalling such a queue removes it for all users.

## Verify
A standard user on an off-network laptop sees the printer, prints a test page, and the job appears in the Universal Print job list in the Azure portal.

## Checked
Date: 2026-11-09. Confirmed in the three Microsoft Learn pages: Discover Universal Print, What is the Universal Print connector, and Universal Print printer provisioning (Intune). Removed as unconfirmed on those pages: licence inclusion, share and permission steps, Settings add-device path, share and cloud device ID requirements, the dsregcmd check, service name, firewall endpoints, event log locations, native printer certificate expiry, driver and finishing limits, document size limits and the secure release notes.
Method: docs-checked 2026-11-09 against the three Microsoft Learn pages listed in sources, downloaded and read in full.
