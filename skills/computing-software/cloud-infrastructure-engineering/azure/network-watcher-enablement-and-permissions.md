---
id: computing-software.cloud-infrastructure-engineering.azure.network-watcher-enablement-and-permissions
name: network-watcher-enablement-and-permissions
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, network-watcher, network-watcher-enable, networkwatcherrg, network-troubleshooting, rbac]
level: practitioner
status: docs-checked
description: "Ensure Network Watcher exists per region, understand automatic enablement, opt out (permanent), delete safely, and grant the actions each Network Watcher tool needs."
sources: ["https://learn.microsoft.com/azure/network-watcher/network-watcher-create", "https://learn.microsoft.com/azure/network-watcher/required-rbac-permissions", "https://learn.microsoft.com/azure/network-watcher/network-watcher-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Network Watcher enablement and permissions

**Goal:** make every Network Watcher tool usable in every region you deploy to, without surprise resource groups or access errors.

## Enablement
- Network Watcher is a regional service, enabled in a region by creating a Network Watcher instance there. By default it is enabled automatically when you create or update a virtual network in the region; this does not affect your resources or charges.
- Portal-created instances are named `NetworkWatcher_{region}` in resource group `NetworkWatcherRG` (created if missing). Azure CLI-created instances are named `{region}-watcher`. To customise the instance name use PowerShell or REST; the resource group must already exist.
```bash
az network watcher list --out table
az group create --name 'NetworkWatcherRG' --location 'eastus'
az network watcher configure --resource-group 'NetworkWatcherRG' --locations 'eastus' --enabled
```
```powershell
New-AzNetworkWatcher -Name 'NetworkWatcher_eastus' -ResourceGroupName 'NetworkWatcherRG' -Location 'eastus'
```
- **Opt out of automatic enablement** (CLI or PowerShell only, not the portal). This is permanent: you cannot opt back in without contacting Azure support, and afterwards you must enable Network Watcher manually in each region you use.
```bash
az feature register --name 'DisableNetworkWatcherAutocreation' --namespace 'Microsoft.Network'
az provider register --name 'Microsoft.Network'
```
- **Disable** a region by deleting its instance: `az network watcher configure --locations 'eastus' --enabled 'false'`. This deletes all running operations, history and alerts with no revert; deleting `NetworkWatcher_eastus` deletes the flow logs, connection monitors and packet captures in East US.

## Permissions
The signed-in account needs Owner, Contributor or Network Contributor, or a custom role with the actions for the capability. Network Contributor does not include the Microsoft.Storage actions (flow logs and additional actions), the Microsoft.Compute actions (additional actions), or the OperationalInsights/Insights DCR and DCE actions (traffic analytics).

| Capability | Actions on the RBAC page |
|---|---|
| Network Watcher | `Microsoft.Network/networkWatchers/read`, `write`, `delete` |
| IP flow verify | `.../networkWatchers/ipFlowVerify/action` and `ipFlowVerify/read` |
| Next hop | `.../networkWatchers/nextHop/action` and `nextHop/read`, plus `Microsoft.Compute/virtualMachines/read` and `Microsoft.Network/networkInterfaces/read` |
| Connection troubleshoot | `.../connectivityCheck/action` and `connectivityCheck/read`, `queryTroubleshootResult/action`, `troubleshoot/action`, `networkConfigurationDiagnostic/read` |
| Packet capture | `.../packetCaptures/` `read`, `write`, `delete`, `stop/action`, `queryStatus/action`, `queryStatus/read` |
| Flow logs | `.../flowLogs/` `read`, `write`, `delete`; `configureFlowLog/action`, `queryFlowLogStatus/action`; `Microsoft.Network/networkSecurityGroups/write` (NSG flow logs only); Storage `listServiceSas`, `listAccountSas`, `listKeys` actions |
| Traffic analytics | all flow log permissions plus read on the network resources listed on the page and workspace/DCR/DCE actions |
Additional actions the page lists: VM and VM scale set read/write and their extensions read/write (to check for and install the Network Watcher extension, run packet captures), `Microsoft.Storage/storageAccounts/Read`, `Microsoft.Authorization/*/Read`, `Microsoft.Insights/alertRules/*`, `Microsoft.Support/*`.
- Traffic analytics creates DCR and DCE resources prefixed `NWTA` in the Log Analytics workspace's resource group; operating on them can break it. Management-group inherited permissions are not supported for enabling traffic analytics.

## Verify
- [ ] `az network watcher list --out table` shows an instance in every region with virtual networks (after an opt-out, one you created yourself).
- [ ] An operator holding only the custom role can run the intended tool without an authorization error.

## Checked

2026-11-07. Read in full: Enable or disable Network Watcher, Azure RBAC permissions for Network Watcher. The Network Watcher overview was fetched but not used for any claim.
- Corrected: the CLI flag is `--locations` (not `-l`), the opt-out is permanent, and CLI-created instances are named `{region}-watcher`.
- Removed (not on the pages read): the `Microsoft.Network/networkWatchers` Bicep route, "two instances per region not allowed", the two built-in policy names, the extension names `NetworkWatcherAgentWindows/Linux`, the `listServiceSas`-only flow log row, and the `az network watcher test-ip-flow` and `--query` Verify steps.
- The CLI reference for `az network watcher` was not read.

Method: documentation only; no commands were run.
