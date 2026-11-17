---
id: computing-software.systems-network-administration.windows-server.wac-in-azure-portal
name: wac-in-azure-portal
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, windows-admin-center, wac, wac-azure-portal, azure-arc, azure-vm, windows-admin-center-administrator-login, azure-rbac, nsg]
level: practitioner
status: docs-checked
description: "Use Windows Admin Center from the Azure portal for Azure VMs and Arc-enabled servers: extension install, the WAC Administrator Login role, networking and limits."
sources:
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/azure/manage-vm
  - https://learn.microsoft.com/en-us/windows-server/manage/windows-admin-center/azure/manage-arc-hybrid-machines
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Windows Admin Center in the Azure portal

**What:** a WAC instance hosted on each machine (as a VM/Arc extension) and opened from the
Azure portal, authenticated with Entra ID and Azure RBAC. No gateway server to run.

## Prerequisites
- Azure VM: Windows Server 2016 or newer, Windows 10 or 11, in an Azure public cloud region (not China, Government or other
  non-public clouds). Outbound HTTPS to the `WindowsAdminCenter` and `AzureActiveDirectory` service tags. Inbound access from the portal to the
  VM's port (6516 by default) is needed; private IP connectivity is recommended over a public IP, and inbound traffic redirected by another service
  (for example Azure Firewall) is not supported.
- Arc-enabled server: Windows Server 2016 or later; no inbound ports are required; outbound access to `*service.waconazure.com` or the
  `WindowsAdminCenter` service tag and outbound 443. The `Microsoft.HybridConnectivity` resource provider is registered during deployment. Arc agent versions 1.35 and 1.36 break the connection; use 1.37+.
- Installing the extension needs Owner or Contributor (Arc: also Windows Admin Center Administrator Login suffices). Connecting needs **Reader** and
  **Windows Admin Center Administrator Login** on the resource; that role uses dataActions, so assign it at subscription, resource group or resource scope, not management group.

## Enable
Portal > VM or Arc machine > Settings > **Windows Admin Center** > Install (deploys the `AdminCenter` extension, publisher
`Microsoft.AdminCenter`) > Connect. If all outbound internet is blocked, add the outbound rule to the WAC service (the install screen has a checkbox for it).
For Arc, the extension can also be deployed with `New-AzConnectedMachineExtension -Name AdminCenter -ExtensionType AdminCenter -Publisher Microsoft.AdminCenter ...`
(settings include the port, 6516 in the doc example; proxy settings need extension version above 0.0.0.321 and authenticated proxies are not supported).
Assign the **Windows Admin Center Administrator Login** role to users at the resource scope in the portal (Access control (IAM)).

## Limits
- Manages only the machine it is installed on, and installing the extension reduces a manually installed multi-server WAC on that machine to single-machine management.
- Third-party extensions are not supported in the portal version; the tool set is the documented essential list (Certificates, Devices, Events, Files, Firewall,
  Installed apps, Local users and groups, Performance Monitor, PowerShell, Processes, Registry, Remote Desktop, Roles and features, Scheduled tasks, Services, Storage, Updates).

## Verify
- [ ] User with the WAC login role can open the server's Overview tool from the portal.
- [ ] For VMs, the inbound rule on 6516 is limited to your management IP addresses (or you use a private IP).

## Checked
Checked 2026-10-26 against Microsoft windowsserverdocs main, Windows Admin Center pages (troubleshooting ms.date 2025-06-24; Azure VM and Arc pages current in repo), Windows Admin Center 2410+.
Confirmed from azure/manage-vm and azure/manage-arc-hybrid-machines (both current in the repo): requirements, service tags, port 6516, no inbound ports for Arc, roles and scope limit, Arc agent 1.35/1.36 issue,
HybridConnectivity provider, AdminCenter extension deployment with New-AzConnectedMachineExtension and proxy limits, tool list and the no-third-party-extension statement.
Corrected the VM networking claim (the service tags are outbound, inbound is from your management IPs or private network) and removed the az vm extension and az role assignment commands and the sign-in mapping text, which the pages do not give.
Method: documentation only; no commands were run.
