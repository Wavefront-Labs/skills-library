---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-native-client-and-tunnel
name: bastion-native-client-and-tunnel
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, bastion-native-client, bastion-tunnel, bastion-ssh, az-network-bastion, entra-login-vm]
level: practitioner
status: docs-checked
description: "Connect through Bastion with native clients: az network bastion ssh/rdp, tunnels for scp and other ports, Entra ID login to VMs, and required roles."
sources: ["https://learn.microsoft.com/azure/bastion/native-client", "https://learn.microsoft.com/azure/bastion/connect-vm-native-client-linux", "https://learn.microsoft.com/azure/bastion/connect-vm-native-client-windows", "https://learn.microsoft.com/cli/azure/network/bastion"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Bastion native client and tunnel

**Goal:** engineers use their own SSH/RDP clients, file transfer and port-forwarding through Bastion, with local SSH keys or
Microsoft Entra ID, no public IPs on the VMs.

## Prerequisites
- Bastion **Standard or Premium** with *Native Client Support* ticked on the Advanced tab or the Configuration page
  (CLI: `az network bastion update --name MyBastionHost --resource-group MyResourceGroup --enable-tunneling`).
- Azure CLI 2.32 or later with the `bastion` extension (`az extension add --name bastion`, update with `az extension update --name bastion`);
  the Windows page also installs the `ssh` extension (`az extension add --name ssh`) for SSH key-pair sign-in.
- The VM's resource ID, and inbound SSH (22), RDP (3389) or your custom port open on the VM.
- Roles for the user: **Reader** on the VM, **Reader** on the NIC with the VM's private IP, **Reader** on the Bastion resource;
  for Entra sign-in also **Virtual Machine Administrator Login** or **Virtual Machine User Login**. For RDP the user must also be a
  local admin or in Remote Desktop Users on the VM.
- Not supported: native client from Cloud Shell, SSH keys stored in Key Vault (download to a local file first), Bastion session recording.

## SSH
```bash
az network bastion ssh --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-resource-id "<VMResourceId>" --auth-type "AAD"
az network bastion ssh --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-resource-id "<VMResourceId>" --auth-type "ssh-key" --username "<Username>" --ssh-key "<Filepath>"
az network bastion ssh --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-ip-address "<VMIPAddress>" --auth-type "ssh-key" --username "<Username>" --ssh-key "<Filepath>"
```
`--auth-type "password" --username "<Username>"` prompts for the password. `az network bastion ssh` does not support file transfer. Connecting by
`--target-ip-address` does not support Entra authentication or custom ports. `--resource-port` sets a custom port.

## RDP (Windows client)
```bash
az network bastion rdp --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-resource-id "<VMResourceId>"
az network bastion rdp --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-resource-id "<VMResourceId>" --enable-mfa
```
The session opens in MSTSC. `--enable-mfa` is for Entra login to Windows 10 20H2+, Windows 11 21H2+ and Windows Server 2022 targets.
Remote connection to Entra-joined VMs is allowed only from Windows 10 or later PCs that are Entra registered (20H1+), joined or hybrid joined
to the same directory as the VM. `--configure` is described as a flag to configure the RDP session. `--resource-port "22"` is the page's
workaround for reaching a Windows VM over port 22 from a Windows client.

## Tunnel (any TCP port, any client)
```bash
az network bastion tunnel --name "<BastionName>" --resource-group "<ResourceGroupName>" --target-resource-id "<VMResourceId>" --resource-port "22" --port "50022"
# other terminal
ssh <username>@127.0.0.1 -p 50022
```
The tunnel relays SSH or RDP (not web servers), works from non-Windows clients and with the client of your choice, and supports
file transfer. Use a local `--port` of 1024 or above without root. The native-client page's table shows no Entra authentication,
no concurrent VM sessions and no custom port for tunnels. The Windows and Linux pages also show a multi-connection tunnel through
`ssh -L 2222:127.0.0.1:22` (not read beyond its steps).

## Verify
- [ ] `az network bastion ssh ... --auth-type AAD` signs you in to an Entra-enabled VM.
- [ ] The tunnel command stays open and the local client connects to `127.0.0.1:<port>`.

## Checked

2026-11-07. Re-read in full: Configure Bastion for native client connections, Connect using a Linux native client, Connect using a Windows native client.
The `az network bastion` CLI reference (35k characters) was searched for `--enable-tunneling`, `--configure`, `--enable-mfa`, `--ssh-key`, `--target-ip-address` and the example lines (not read end to end).
- Removed (not on any page): AADSSHLoginForLinux and AADLoginForWindows extension names, "Reader on the VNet" (pages say Reader on the NIC), `scp -P` example, RDP from macOS, "`--configure` opens an .rdp you can edit", the "not authorized" gotcha, the Standard-SKU-for-file-transfer gotcha as worded, the original Verify step about diagnostic logs and `user@contoso.com`.
- Added from pages: connection-method table facts, unsupported cases, MFA OS versions, local-port rule.
- Not read: the file-transfer page and the NSG-rule details the native-client page refers to.

Method: documentation only; no commands were run.
