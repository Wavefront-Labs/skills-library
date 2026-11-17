---
id: computing-software.cloud-infrastructure-engineering.azure.p2s-vpn-entra-id-authentication
name: p2s-vpn-entra-id-authentication
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, vpn-gateway, point-to-site, p2s-entra-id, vpn-entra-auth, azure-vpn-client, openvpn]
level: advanced
status: docs-checked
description: "Configure point-to-site VPN with Microsoft Entra ID authentication using the Microsoft-registered Azure VPN Client app, Conditional Access/MFA, and client profile distribution."
sources: ["https://learn.microsoft.com/azure/vpn-gateway/point-to-site-entra-gateway", "https://learn.microsoft.com/azure/vpn-gateway/point-to-site-entra-vpn-client-windows", "https://learn.microsoft.com/azure/vpn-gateway/openvpn-azure-ad-mfa"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# P2S VPN with Microsoft Entra ID authentication

**Goal:** let users connect to Azure VNets with their Entra identity and MFA instead of certificates.

## Prerequisites
- A VPN gateway that is not the Basic SKU and not policy-based.
- Tunnel type **OpenVPN (SSL)** with authentication type Microsoft Entra ID.
- Client: Azure VPN Client; the audience table on the gateway page lists Windows and macOS.

## Configure
1. Use the **Microsoft-registered** Azure VPN Client app: audience `c632b3df-fb67-4d84-bdcf-b95ad541b5c8` (new setups). The older manually registered app ID `41b23e61-6c1e-4545-b367-cd054e0ed4b4` (Azure Public) retires on March 31, 2028 in Azure Public, so migrate to the Microsoft-registered one.
2. Gateway point-to-site configuration:
```bash
az network vnet-gateway update -g rg -n vpngw \
  --address-prefixes 172.16.201.0/24 --client-protocol OpenVPN \
  --aad-tenant https://login.microsoftonline.com/<tenantId>/ \
  --aad-audience c632b3df-fb67-4d84-bdcf-b95ad541b5c8 \
  --aad-issuer https://sts.windows.net/<tenantId>/
```
   The tenant URL must not end with a backslash (a forward slash is fine); the issuer must end with a trailing slash or the connection might fail.
3. Restrict who can connect: on the Enterprise application for Azure VPN, set "User assignment required?" to Yes and assign users or groups.
4. MFA: Conditional Access is the recommended way to require it for the VPN.
5. Download the profile (`az network vnet-gateway vpn-client generate`) and import it into the Azure VPN Client.

## Gotchas
- Address pool must not overlap the virtual network or the on-premises location. The minimum subnet mask is /29 for active/passive and /28 for active/active.
- Custom routes, custom DNS and forced tunneling are optional Azure VPN Client settings.

## Verify
- [ ] Client connects and receives an IP address from the pool.
- [ ] Sign-in logs show the Azure VPN app with the CA policy applied.

## Checked
2026-10-31. Confirmed on Microsoft Learn (P2S Entra gateway, Azure VPN Client for Windows, OpenVPN Entra MFA pages): Microsoft-registered audience `c632b3df-fb67-4d84-bdcf-b95ad541b5c8`, manual app ID and retirement date, Basic SKU and policy-based gateways unsupported, OpenVPN (SSL) tunnel type, tenant and issuer URL rules, address pool mask limits, user assignment setting, Conditional Access for MFA, `az network vnet-gateway update` flags (CLI reference). Removed: VpnGw1 minimum, Linux/iOS/Android client list, Intune, B2B guest, mixed cert/Entra and `--custom-routes` claims.
Method: documentation only; no commands were run.
