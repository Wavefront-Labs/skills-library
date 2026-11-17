---
id: computing-software.systems-network-administration.windows-server.nps-radius-clients
name: nps-radius-clients
category: computing-software
field: systems-network-administration
product: windows-server
tags: [windows-server, nps, network-policy-server, radius-clients, new-npsradiusclient, shared-secret, register-nps-in-ad, ras-and-ias-servers, netsh-nps, radius]
level: practitioner
status: docs-checked
description: "Set up NPS as a RADIUS server: register in AD, add RADIUS clients with strong per-device shared secrets, export/import config between NPS servers, and checks."
sources:
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-manage-install
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-radius-clients-configure
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-udp-ports-configure
  - https://learn.microsoft.com/en-us/windows-server/networking/technologies/nps/nps-radius-clients
  - https://learn.microsoft.com/en-us/powershell/module/nps/new-npsradiusclient
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NPS RADIUS clients

## Install and register
```powershell
Install-WindowsFeature NPAS -IncludeManagementTools
```
Register NPS in Active Directory so it can read user dial-in properties; registration adds the server to the **RAS and IAS Servers** group.
To register in another domain: `netsh nps add registeredserver <domain> <server>`.

## Add RADIUS clients (switches, WLCs, VPN servers)
```powershell
New-NpsRadiusClient -Name 'wlc-lon-01' -Address 10.0.5.10 -SharedSecret '<RANDOM_SECRET>' -VendorName 'RADIUS Standard'
Get-NpsRadiusClient
```
- `-Address` takes an FQDN or IP address. IP address ranges are a console feature of Windows Server Datacenter (not Standard) per the 2016 docs; all clients in a range share one configuration and secret.
- Configure the same strong shared secret on the NAS; the console can generate one. When Message Authenticator is used, the secret also keys the message protection; the attribute is required and enabled by default for EAP.
- Standard RADIUS ports are UDP 1812 (authentication) and 1813 (accounting); NPS listens by default on 1812, 1813, 1645 and 1646, and installing NPS creates the Windows Firewall exceptions.
- Point each network device at two NPS servers for redundancy.

## Keep NPS servers in sync
Export on one server and import on the others (see nps-export-import-configuration). The export contains unencrypted shared secrets: protect it.

## Verify
- [ ] `Get-NpsRadiusClient` shows the same clients on both NPS servers.
- [ ] A test authentication from the device reaches NPS (check the Network Policy and Access Services logs or accounting).

## Checked

2026-10-25, against the MicrosoftDocs/windowsserverdocs repository (main, last commit 2026-10-23), the windows-powershell-docs NPS cmdlet pages and the MicrosoftDocs/entra-docs repository. Confirmed Install-WindowsFeature NPAS, netsh nps add registeredserver and the RAS and IAS Servers group, New-NpsRadiusClient parameters, the Datacenter-only IP range rule (Windows Server 2016 wording), ports 1812/1813/1645/1646 with automatic firewall exceptions, and the Message Authenticator note. Removed the unconfirmed CIDR example, Standard client limits and device test commands.

Method: documentation only; no commands were run.
