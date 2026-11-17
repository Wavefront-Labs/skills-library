---
id: computing-software.systems-network-administration.windows-server.azure-arc-vm-extensions
name: azure-arc-vm-extensions
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-arc, arc-extensions, new-azconnectedmachineextension, custom-script-extension, azure-monitor-agent]
level: practitioner
status: docs-checked
description: "Deploy and manage VM extensions on Azure Arc-enabled servers: Azure Monitor Agent, Custom Script, Defender, extension allowlists and troubleshooting failed installs."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/manage-vm-extensions
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/security-extensions
  - https://learn.microsoft.com/en-us/powershell/module/az.connectedmachine/new-azconnectedmachineextension
  - https://learn.microsoft.com/en-us/powershell/module/az.connectedmachine/update-azconnectedextension
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/agent-overview
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# VM extensions on Arc-enabled servers

## Install (Az.ConnectedMachine)
```powershell
New-AzConnectedMachineExtension -ResourceGroupName <rg> -MachineName <machine> -Location <region> `
  -Name AzureMonitorWindowsAgent -Publisher Microsoft.Azure.Monitor -ExtensionType AzureMonitorWindowsAgent `
  -EnableAutomaticUpgrade
New-AzConnectedMachineExtension -ResourceGroupName <rg> -MachineName <machine> -Location <region> `
  -Name CustomScriptExtension -Publisher Microsoft.Compute -ExtensionType CustomScriptExtension `
  -Setting @{commandToExecute='powershell -ExecutionPolicy Bypass -File inventory.ps1'; fileUris=@('https://<storage>/inventory.ps1')}
```
Extensions are the same as for Azure VMs and are published by Microsoft and selected third parties. Regular settings
are stored in Azure; protected settings (`-ProtectedSetting`) are not persisted in Azure and are encrypted at rest on
the machine. Many extensions support automatic upgrade. Every install, update or upgrade is an Azure API call and is
recorded in the Azure Monitor Activity Log.

## List, update, remove
```powershell
Get-AzConnectedMachineExtension -ResourceGroupName <rg> -MachineName <machine>
Update-AzConnectedExtension -ResourceGroupName <rg> -MachineName <machine> -ExtensionTarget @{'Microsoft.Azure.Monitor.AzureMonitorWindowsAgent'=@{targetVersion='<version>'}}
Remove-AzConnectedMachineExtension -ResourceGroupName <rg> -MachineName <machine> -Name CustomScriptExtension
```
If an extension is removed locally but Azure still expects it, it is reinstalled at the next sync.

## Lock it down on the server
```cmd
azcmagent config set extensions.allowlist "Microsoft.Azure.Monitor/AzureMonitorWindowsAgent,Microsoft.Azure.AzureDefenderForServers/MDE.Windows"
azcmagent config set extensions.blocklist "Microsoft.Compute/CustomScriptExtension"
azcmagent config set extensions.allowlist "Allow/None"     :: extension manager runs, nothing installs
azcmagent config set extensions.enabled false              :: disable the extension manager
azcmagent config list
```
Allow and block lists are local to each server and cannot be overridden from Azure, even by an Owner; an
unauthorized extension is refused and reported as a failed install. With no list, all extensions are allowed. Allow
lists beat block lists because they also block extensions published later. Custom Script and Run Command run as Local
System, so block them where not needed.

## Troubleshoot
- Logs: `%ProgramData%\GuestConfig\ext_mgr_logs\gc_ext.log` (extension manager) and
  `%ProgramData%\GuestConfig\extension_logs` (one folder per extension).
- `azcmagent show` must report connected; the `ExtensionService` service must be running.
- Extensions download from Azure Storage (`*.blob.core.windows.net`, which changes regularly) unless private
  endpoints are used, in which case they are proxied through the regional Arc URL.

## Verify
- [ ] Extension shows Succeeded in the portal and the workload (for example heartbeat in Log Analytics) works.

## Checked
Date 2026-10-27. Documentation: Arc extension security and management pages, agent overview (log paths),
Az.ConnectedMachine New-AzConnectedMachineExtension and Update-AzConnectedExtension references. Confirmed: cmdlet
parameters, config keys and allow/block list semantics, log paths, download endpoints, local-removal behaviour.
Method: documentation only; no commands were run.
