---
id: computing-software.systems-network-administration.patch-management.patching-remote-and-roaming-endpoints
name: patching-remote-and-roaming-endpoints
category: computing-software
field: systems-network-administration
product: patch-management
tags: [remote-endpoint-patching, cloud-management-gateway, windows-update-client-policies, delivery-optimization, intune, patch-deployment]
level: practitioner
status: docs-checked
description: "Patch remote Windows laptops: Windows Update client policies (deferral, pause, deadlines), the ConfigMgr cloud management gateway, and Delivery Optimization scope."
sources:
  - https://learn.microsoft.com/en-us/mem/configmgr/core/clients/manage/cmg/overview
  - https://learn.microsoft.com/en-us/windows/deployment/update/waas-manage-updates-wufb
  - https://learn.microsoft.com/en-us/windows/deployment/do/waas-delivery-optimization
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Patching remote and roaming endpoints

**Goal:** devices that rarely touch the corporate network get updates through a path that does not depend on the office network.

## Choose the delivery path
- **Windows Update client policies (formerly Windows Update for Business)**: devices connect directly to the Windows Update service; Group Policy or MDM such as Intune sets the policies. Available for Pro (including Workstations), Education and Enterprise editions of Windows 10 and 11.
- **ConfigMgr with a cloud management gateway (CMG)**: a CMG is a cloud service in Azure that lets clients on the internet use on-premises site roles without exposing that infrastructure. Documented management activities include software updates, inventory and client status, compliance settings, software distribution and in-place upgrade task sequences. Domain-joined clients use PKI certificates; Entra-joined or hybrid clients can authenticate with Entra ID.
- **Windows Autopatch**: a cloud service that works with the client policies and adds control over approval, scheduling and safeguarding of updates.

## Enforcement controls (Windows Update client policies)
- Deferral: quality updates up to 30 days, feature updates up to 365 days, counted from when the update is first made available on Windows Update. Feature deferral uses "Select when Preview Builds and feature updates are Received"; quality uses "Select when Quality Updates are Received".
- Pause: 35 days from a start date you set; pausing feature updates still lets quality updates through.
- Compliance deadline policy: separate deadline (days from publication) and grace period (days from install until a forced restart) for feature and quality updates. The page suggests this suits users returning from leave.
- Microsoft's guidance is to use fewer controls: Windows Update has built-in intelligence, and defaults (automatic download, install and restart) plus deadlines are the recommended experience settings.
- Device recommendations from the page: used at least 6 hours a month including 2 hours continuous, at least 10 GB free space, charged regularly, unobstructed access to the Windows Update service.

## Delivery Optimization
- Reliable HTTP downloader that can also source content from peers and Microsoft Connected Cache, falling back to HTTP; peer-to-peer is optional. Needs internet access and Delivery Optimization cloud services for peering and Connected Cache.
- On Windows client Enterprise, Professional and Education editions peering on the local NAT is on by default (download mode 1); Windows Server 2019 or later defaults to download mode 0.
- Covers Windows Update content, Microsoft 365 apps, Edge, Defender definitions, Intune Win32 apps (peer and cache support there is public cloud only) and Configuration Manager express updates.

## Visibility
Windows Update for Business reports (Azure portal) covers Entra-joined devices: monitor security, quality, driver and feature updates and list devices with update compliance issues.

## Gotchas
- A CMG is used by default by all clients when they are internet-based; scope it with the "Enable clients to use a cloud management gateway" client setting if needed.
- Office installed as Click-to-Run cannot be updated through Windows Update client policies; MSI-installed Office can, once Microsoft product updates are turned on (off by default).
- Driver updates are on by default and can be turned off with the policies.

## Verify
Per-device update status in Windows Update for Business reports or your management console shows remote devices on the current quality update within your deadline; set your own latency target.

## Checked
Date: 2026-11-07. Read in full: Cloud management gateway overview, Windows Update client policies (the page the old WUfB URL redirects to) and What is Delivery Optimization. Removed as unconfirmed: VPN split-tunnel exclusion advice, the 0-7 day deferral, 2-3 day deadline and 1-2 day grace example values, `DODownloadMode 1` as a recommendation for home sites, the 14-day non-compliance rule, Conditional Access minimum OS build, the metered-connection setting, WSUS dual-scan advice, macOS declarative updates, and the "Download delta content when available" CMG advice (the CMG page does not mention it).
Method: documentation only; no commands were run.
