---
id: computing-software.cloud-infrastructure-engineering.azure.azure-monitor-agent-windows-client-installer
name: azure-monitor-agent-windows-client-installer
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-monitor-agent, windows-client-installer, intune, monitored-object, windows-11]
level: practitioner
status: docs-checked
description: "Install Azure Monitor Agent on Windows 10/11 client devices with the MSI installer, create the monitored object, associate DCRs and deploy at scale with Intune."
sources: ["https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent-windows-client", "https://learn.microsoft.com/azure/azure-monitor/agents/azure-monitor-agent-requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AMA on Windows client devices

**Goal:** collect event logs and performance data from Entra-joined Windows 10/11 PCs (not servers, not Arc) into Log Analytics.

## Prerequisites
- Windows 10 or 11 client, Microsoft Entra joined or hybrid joined (see the supported-OS table on Learn for versions).
- Tenant-level setup: an Azure tenant admin might be required.
- Devices must reach the AMA endpoints (or AMPLS).

## Steps
1. **Install** the MSI on devices (Intune Win32 app or line-of-business app):
```
msiexec /i AzureMonitorAgentClientSetup.msi /qn
```
   Proxy: `msiexec /i AzureMonitorAgentClientSetup.msi /qn PROXYUSE=true PROXYADDRESS=http://proxy:3128 PROXYUSEAUTH=false`.
2. **Grant** your admin identity the `Monitored Objects Contributor` role at tenant root scope (`/providers/Microsoft.Insights`) via `az role assignment create ... --scope "/providers/Microsoft.Insights"` (requires elevated access).
3. **Create the monitored object** for the tenant (one per Entra tenant; its region must match the DCR region):
```
PUT https://management.azure.com/providers/Microsoft.Insights/monitoredObjects/<tenantId>?api-version=2021-09-01-preview
{ "properties": { "location": "eastus" } }
```
4. **Associate** your DCR with the monitored object:
```
PUT https://management.azure.com/providers/Microsoft.Insights/monitoredObjects/<tenantId>/providers/microsoft.insights/datacollectionruleassociations/assoc1?api-version=2021-09-01-preview
{ "properties": { "dataCollectionRuleId": "<dcrId>" } }
```
   All devices in the tenant with the agent get every DCR associated with the monitored object.

## Gotchas
- Association is tenant-wide; scope data volume with the DCR (XPath filters), not by device.
- The client installer (MSI) is a separate install path from the VM extension.

## Verify
- [ ] The agent is installed on a test device and data from the DCR arrives in the workspace.

## Checked

Date: 2026-10-28.

Confirmed against Learn (AMA Windows client): MSI install and proxy parameters PROXYUSE/PROXYADDRESS/PROXYUSEAUTH, Monitored Objects Contributor role (name corrected), monitored object per tenant in the DCR's region, DCR association via monitoredObjects with a unique association name, tenant-wide scope of DCRs for client devices.
Removed: Windows 10 build and architecture list, Global Admin wording, TLS-inspection claim, VM-extension warning, Heartbeat query and Control Panel check (not on fetched pages).

Method: documentation only; no commands were run.
