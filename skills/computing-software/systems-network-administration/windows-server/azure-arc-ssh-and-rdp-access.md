---
id: computing-software.systems-network-administration.windows-server.azure-arc-ssh-and-rdp-access
name: azure-arc-ssh-and-rdp-access
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, azure-arc, arc-ssh, ssh-over-arc, openssh, entra-id-login]
level: practitioner
status: docs-checked
description: "Connect to Arc-enabled Windows servers with SSH (and RDP tunnelled over SSH) through Azure without inbound ports, using az ssh arc and Entra ID or local credentials."
sources:
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/ssh-arc-overview
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/ssh-arc-powershell-remoting
  - https://learn.microsoft.com/en-us/cli/azure/ssh
  - https://learn.microsoft.com/en-us/azure/azure-arc/servers/network-requirements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# SSH and RDP to Arc-enabled servers

SSH for Arc needs no public IP address or open inbound ports: the connection goes through Azure.

## Prepare the server
Agent version 1.31 or higher. OpenSSH Server must be installed and running (installed by default from Windows
Server 2025):
```powershell
Get-WindowsCapability -Online | Where-Object Name -like 'OpenSSH*'
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Set-Service sshd -StartupType Automatic; Start-Service sshd
```
Enable the connectivity endpoint and SSH service configuration (once per machine, API version 2023-03-15):
```bash
az rest --method put --uri "https://management.azure.com/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.HybridCompute/machines/<machine>/providers/Microsoft.HybridConnectivity/endpoints/default?api-version=2023-03-15" --body '{"properties":{"type":"default"}}'
az rest --method put --uri "https://management.azure.com/subscriptions/<sub>/resourceGroups/<rg>/providers/Microsoft.HybridCompute/machines/<machine>/providers/Microsoft.HybridConnectivity/endpoints/default/serviceconfigurations/SSH?api-version=2023-03-15" --body '{"properties":{"serviceName":"SSH","port":22}}'
```
To switch the feature off on the server: `azcmagent config set incomingconnections.enabled false`.

## Connect
```bash
az extension add --name ssh
az ssh arc --resource-group <rg> --name <machine> --local-user <username>
```
Az.Ssh (`Install-Module -Name Az.Ssh`) provides the PowerShell equivalent. Local-user login needs `--local-user`;
Microsoft recommends Microsoft Entra issued certificates where available. The Entra login extension described in
the overview is for Linux (AADSSHLoginForLinux).

RDP: `az ssh arc` has `--rdp` and `--winrdp` options that tunnel RDP over the SSH connection (see the az ssh
reference for their exact behaviour).

PowerShell remoting over SSH: generate a config with
`az ssh config --resource-group <rg> --name <machine> --local-user <user> --resource-type Microsoft.HybridCompute --file <config-file>`,
then use `New-PSSession -HostName <machine> -UserName <user> -Options $options` with the ProxyCommand from that
file (see the PowerShell remoting page).

## Permissions
- Entra authentication uses the Azure roles **Virtual Machine Administrator Login** and **Virtual Machine User
  Login** (dataActions). Owner or Contributor does not grant login by itself. Assign them at management group,
  subscription or resource-group scope rather than per VM, and consider Privileged Identity Management.

## Gotchas
- Proxies and firewalls must allow the Arc service endpoints listed in the network requirements, including the
  `*.servicebus.windows.net` and `*.guestnotificationservice.azure.com` entries.

## Verify
- [ ] `az ssh arc` opens a prompt with no inbound firewall rule on the server.

## Checked
Date 2026-10-27. Documentation: Arc SSH overview and PowerShell remoting pages, az ssh CLI reference, network
requirements. Confirmed: agent minimum, OpenSSH notes, REST calls and API version, `az ssh arc` parameters including
`--local-user` and `--rdp`, Entra roles, relay endpoints, disable setting.
Method: documentation only; no commands were run.
