---
id: computing-software.cloud-infrastructure-engineering.azure.bastion-ip-based-connection-and-kerberos
name: bastion-ip-based-connection-and-kerberos
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, bastion, ip-based-connection, bastion-kerberos, on-premises-rdp, domain-joined-vms]
level: practitioner
status: docs-checked
description: "Use Azure Bastion to reach machines by private IP (peered VNets, on-prem over VPN/ExpressRoute) and enable Kerberos authentication for domain-joined Windows targets."
sources: ["https://learn.microsoft.com/azure/bastion/connect-ip-address", "https://learn.microsoft.com/azure/bastion/kerberos-authentication-portal", "https://learn.microsoft.com/azure/bastion/configuration-settings", "https://learn.microsoft.com/cli/azure/network/bastion"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bastion IP-based connection and Kerberos

**Goal:** one Bastion reaches Azure VMs and on-prem servers by IP, with domain (Kerberos) logins.

## IP-based connection
- Needs the **Standard SKU or higher** (Basic and Developer do not support it), and the IP-based connection setting must be
  enabled on the Bastion Configuration page. CLI:
```bash
az network bastion update --name MyBastionHost --resource-group MyResourceGroup --enable-ip-connect true
```
- Portal: the Bastion Connect page lets you target an IP address for RDP or SSH in the browser.
- Native client (`rdp`, `ssh` and `tunnel` are CLI extension commands, each with `--target-ip-address`):
```bash
az network bastion rdp --name MyBastionHost --resource-group MyResourceGroup --target-ip-address 10.0.0.1
az network bastion ssh --name MyBastionHost --resource-group MyResourceGroup --target-ip-address 10.0.0.1 --auth-type password --username xyz
az network bastion tunnel --name MyBastionHost --resource-group MyResourceGroup --target-ip-address 10.0.0.1 --resource-port 22 --port 50022
```
- Targets: on-premises VMs (ExpressRoute private peering or site-to-site VPN), VMs in other clouds reachable the same way, and
  Azure VMs in a peered or connected VNet.
- Limitations (page): no force tunnelling over VPN and no default route advertised over ExpressRoute (traffic is dropped, Bastion
  needs internet access); Microsoft Entra authentication is not supported for RDP by IP (SSH via native client is); custom
  ports and protocols are not supported with the native client; UDRs are not supported on the Bastion subnet.

## Kerberos authentication
For domain-joined Windows VMs, Bastion can use Kerberos instead of NTLM (Basic SKU or higher; configurable in the portal only,
not through the native client):
1. Set the VNet's DNS servers to *Custom* with the IP of your Azure-hosted domain controller **before** deploying Bastion.
   Later DNS changes do not propagate to Bastion: delete and re-create the Bastion resource.
2. Deploy Bastion with *Kerberos* ticked on the Advanced tab, or for an existing Bastion go to Configuration, select
   *Kerberos authentication* and Apply.
3. NSGs on the Bastion and the domain controllers must allow both inbound and outbound traffic on ports 53, 88, 389, 464 and 636.
4. Sign in with the user principal name (UPN), e.g. `user@contoso.com`.
- Considerations: the domain controller must be an Azure-hosted VM in the same VNet as Bastion; migrated on-premises VMs
  and cross-realm authentication are not supported; if more DCs are added Bastion only recognises the first, and DCs of
  other domains cannot authenticate with Kerberos.
- Enabling Kerberos does not stop fallback to NTLM. To prove it is used, on the target VM set the local policy *Network security:
  Restrict NTLM: Incoming NTLM traffic* to *Deny all domain accounts* and reconnect: success means Kerberos worked.

## Verify
- [ ] After the NTLM-deny policy above, signing in through Bastion with the UPN still succeeds.
- [ ] `az network bastion rdp ... --target-ip-address <ip>` opens a session to a reachable machine.

## Checked

2026-11-07. Re-read in full: Bastion IP-based connection, Kerberos (portal) article including its ARM template, Bastion configuration settings.
The `az network bastion` CLI reference (35k characters) was searched for `--enable-ip-connect`, `--target-ip-address`, `--auth-type`, `--username`, `--resource-port` and `--port` and the examples (not read end to end).
- Removed (not on any page): "Reader on Bastion is enough" RBAC claim, the `MicrosoftAzureBastionAuditLogs` log name, the asymmetric-routing gotcha, the claim that UDRs/firewalls must allow RDP/SSH from the Bastion subnet, the portal path "Connect via IP address", and the original Verify step about audit logs.
- Corrected: Kerberos ports were 88/53/389; the page lists 53, 88, 389, 464 and 636. SKU for IP connect is Standard or higher, Kerberos Basic or higher.
- Added from pages: limitations list and the NTLM-deny verification procedure.

Method: documentation only; no commands were run.
