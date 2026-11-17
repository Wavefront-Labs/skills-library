---
id: computing-software.cloud-infrastructure-engineering.azure.arc-enabled-server-ssh-run-command-and-extensions-allowlist
name: arc-enabled-server-ssh-run-command-and-extensions-allowlist
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-arc, arc-ssh, arc-run-command, arc-machine-configuration, extensions-allowlist, hybrid-servers]
level: practitioner
status: docs-checked
description: "Manage Arc-enabled servers: SSH without open ports, Run Command and its RBAC, and locking the agent down with extension allow/block lists and monitor mode."
sources: ["https://learn.microsoft.com/azure/azure-arc/servers/ssh-arc-overview", "https://learn.microsoft.com/azure/azure-arc/servers/run-command", "https://learn.microsoft.com/azure/azure-arc/servers/security-extensions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Arc-enabled server management

**Goal:** operate on-premises or other-cloud servers from Azure without inbound firewall holes, with the agent locked to only the features you use.

## SSH through Arc
- No public IP address or open SSH port is required. Works for Windows and Linux; sign in as a local user, or as an Azure (Entra) user on Linux only.
- Prerequisites: Owner or Contributor on the Arc server; hybrid agent version 1.31 or higher; `sshd` enabled (Windows Server 2025 installs OpenSSH by default).
- One time per subscription, register the resource provider and add the CLI extension:
```bash
az provider show -n Microsoft.HybridConnectivity -o tsv --query registrationState
az provider register -n Microsoft.HybridConnectivity
az extension add --name ssh
```
Registration can take 2-5 minutes. The default connectivity endpoint is normally created automatically at first connection.
- The connectivity endpoint's service configuration allows SSH to a single port (default 22). The CLI tools try to set it at runtime; you can set it manually with `az rest` against `.../providers/Microsoft.HybridConnectivity/endpoints/default/serviceconfigurations/SSH`. There may be a delay before you can connect. See the `az ssh` reference for connect examples.
- Entra login on Linux needs the `AADSSHLoginForLinux` extension (installs `aadsshlogin`) plus the role Virtual Machine Administrator Login or Virtual Machine User Login. Owner or Contributor does not grant Entra login. Assign these roles at management group, subscription or resource group scope rather than per machine, to avoid the role-assignment limit.
- To disable all remote access, run on the machine: `azcmagent config set incomingconnections.enabled false`.

## Run Command
```bash
az connectedmachine run-command create --name "myRunCommand" --machine-name "myMachine" --resource-group "myRG" --script "Write-Host Hello World!"
az connectedmachine run-command show --name "myRunCommand" --machine-name "myMachine" --resource-group "myRG"
az connectedmachine run-command list --machine-name "myMachine" --resource-group "myRG"
az connectedmachine run-command delete --name "myRunCommand" --machine-name "myMachine" --resource-group "myRG"
```
- Reading needs `Microsoft.HybridCompute/machines/runCommands/read` (Reader and up). Running needs `Microsoft.HybridCompute/machines/runCommands/write` (Azure Connected Machine Resource Administrator and up): treat that action as admin-equivalent.
- To stop it locally, block the Run Command handlers with `extensions.blocklist` (for example `microsoft.cplat.core/runcommandhandlerwindows`).

## Lock down the agent
```bash
azcmagent config set extensions.allowlist "Microsoft.Azure.Monitor/AzureMonitorLinuxAgent"
azcmagent config set guestconfiguration.enabled false
azcmagent config set config.mode monitor
azcmagent config list
azcmagent config set extensions.enabled false
```
- Default is full mode: all extensions allowed unless restricted by allow lists, block lists or Azure Policy.
- Monitor mode allows only monitoring and security extensions (for example Azure Monitor Agent, Microsoft Defender for Cloud), blocks extensions that could change system configuration or run scripts, and disables the guest configuration policy agent. Microsoft updates the monitor-mode list; read it with `azcmagent config list`.
- In monitor mode you cannot edit the allow or block list: switch back with `azcmagent config set config.mode full`.
- `extensions.allowlist "Allow/None"` allows no extensions; `extensions.enabled false` disables the extension manager entirely.
- Run `azcmagent config set` locally on each machine.

## Verify
- [ ] SSH works with no inbound rule; `azcmagent config list` shows the intended allowlist and mode.

## Checked

Method: docs-checked 2026-11-09 against the Learn pages ssh-arc-overview, run-command and security-extensions (read in full or the relevant sections; run-command and security-extensions by keyword). Removed unconfirmed claims: the `az ssh arc` command line and its flags, `incomingconnections.ports`, `--location` and `--async-execution` on Run Command, root/SYSTEM execution, machine configuration billing and the silent extension failure message.
