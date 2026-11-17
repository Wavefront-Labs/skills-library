---
id: computing-software.systems-network-administration.virtualisation.azure-local-vs-windows-server-hyper-v
name: azure-local-vs-windows-server-hyper-v
category: computing-software
field: systems-network-administration
product: virtualisation
tags: [azure-local, azure-stack-hci, hyper-v, windows-server, licensing]
level: practitioner
status: docs-checked
description: "Choose between Azure Local (formerly Azure Stack HCI) and Windows Server Hyper-V: licensing, Azure connection, hardware, management and guest licensing differences."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/compare-windows-server
  - https://learn.microsoft.com/en-us/azure/azure-local/concepts/billing
  - https://learn.microsoft.com/en-us/azure/azure-local/manage/vm-activate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Local vs Windows Server Hyper-V

**Goal:** pick the right platform for an on-premises Hyper-V estate before buying hardware and licences.

## Comparison
| | Azure Local (formerly Azure Stack HCI) | Windows Server with Hyper-V |
|---|---|---|
| Host licensing | Billed through your Azure subscription per physical core; pay as you go or Azure Hybrid Benefit | Traditional licences or Windows Server Pay-as-You-Go |
| Azure connection | Required: connect to Azure at least once every 30 days so core counts can be billed. Disconnected operations (a locally hosted control plane) is a separate, newer option | Optional (required only for Azure Arc or Pay-as-You-Go) |
| Hardware | Pre-validated solutions from the Azure Local Catalog | Hardware with the "Certified for Windows Server" logo |
| Storage | Storage Spaces Direct; the documentation also describes SAN-based (disaggregated) deployments | Storage Spaces Direct, SANs and other flexible architectures |
| Preferred host tool | Azure portal | Windows Admin Center |
| VM management | Azure portal through Azure Arc, Windows Admin Center, PowerShell | Windows Admin Center, PowerShell, Server Manager, optionally Azure Arc |
| Workloads on the host | Run everything inside VMs or containers, not directly on the cluster; no CAL licensing for direct client connections | Server roles and apps can run directly, with CALs |
| Guest Windows licensing | Windows Server subscription add-on, Azure Hybrid Benefit or bring your own licence | Standard: 2 VMs included; Datacenter: unlimited VMs |
| Included extras | Built-in AKS, Azure Update Manager included, Extended Security Updates included | Installable AKS (being retired in stages, see the comparison page), Update Manager via Azure Hybrid Benefit |

## Choosing
- **Azure Local:** Azure-centric operations, Arc VM management, accepting the Azure billing model and the 30-day connection requirement.
- **Windows Server:** directly hosted roles, SAN-based or other flexible storage, or hardware outside the Azure Local catalog.

## Gotchas
- Azure Local is a host platform: it is not licensed for CAL-based client access, so keep server roles in VMs.
- Azure Local supports Automatic VM Activation; with a Windows Server subscription it is enabled automatically on the hosts.
- Check the comparison page for the current feature table before deciding; it changes with each Azure Local release.

## Verify
Write down the cost of both options over your planning horizon using current pricing pages, the connectivity requirements and the management tools the team will actually use before deciding.

## Checked

Date checked: 2026-10-27. Documentation: Azure Local comparison, billing and VM activation pages in the Azure Stack documentation repository (comparison page dated 2026-03-02; applies to Azure Local 2311.2 and later and Windows Server 2025).
Confirmed: 30-day connection requirement and per-core Azure billing; licensing options and 2/unlimited guest VMs; hardware catalogue versus certified hardware; Azure portal and Windows Admin Center as preferred tools; no CALs on Azure Local; AVMA support. Disconnected operations and SAN-based deployments are described in the billing and comparison pages.

Method: documentation only; no commands were run.
