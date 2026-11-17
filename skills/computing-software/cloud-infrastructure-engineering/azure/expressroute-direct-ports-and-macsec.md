---
id: computing-software.cloud-infrastructure-engineering.azure.expressroute-direct-ports-and-macsec
name: expressroute-direct-ports-and-macsec
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, expressroute, er-direct-ports, macsec, expressroute-direct, letter-of-authorization]
level: sme
status: docs-checked
description: "Provision ExpressRoute Direct 10/100 Gbps port pairs, get the LOA, carve circuits, and enable MACsec with CAK/CKN secrets in Key Vault."
sources: ["https://learn.microsoft.com/azure/expressroute/expressroute-erdirect-about", "https://learn.microsoft.com/azure/expressroute/expressroute-howto-erdirect", "https://learn.microsoft.com/azure/expressroute/expressroute-howto-macsec"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ExpressRoute Direct ports and MACsec

**Goal:** connect directly to Microsoft's edge at a peering location at 10 or 100 Gbps, with link-layer encryption.

## When Direct fits
- Over 10 Gbps aggregate, or regulatory need for physical isolation / MACsec.
- You (or your colo partner) can run cross-connects at a Microsoft peering location.
- You want to carve multiple circuits (for example 5 x 10 Gbps on a 100 Gbps pair) and own the port bandwidth.

## Provision
```powershell
Get-AzExpressRoutePortsLocation                          # locations and available bandwidths
New-AzExpressRoutePort -Name erd1 -ResourceGroupName rg -PeeringLocation "<location>" `
  -BandwidthInGbps 100 -Encapsulation QinQ -Location westeurope   # QinQ or Dot1Q, fixed at create
New-AzExpressRoutePortLOA -ExpressRoutePort (Get-AzExpressRoutePort -Name erd1 -ResourceGroupName rg) `
  -CustomerName "Contoso" -Destination ".\loa.pdf"
```
Give the Letter of Authorization to the colo to order the two cross-connects (primary and secondary port). Then set both links `AdminState = Enabled`.

Create circuits on the port: `New-AzExpressRouteCircuit ... -ExpressRoutePort $port -BandwidthInGbps 10 -SkuTier Premium -SkuFamily MeteredData`. The circuit sizes allowed on each port speed, and the oversubscription rules, are on the ExpressRoute Direct overview page.

## MACsec
1. Create Key Vault secrets for CKN and CAK (hex strings: CKN even length up to 64, CAK 32 or 64 hex chars to match the cipher).
2. Give a user-assigned managed identity `get` on secrets, attach it to the port (`New-AzExpressRoutePortIdentity`).
3. Set on each link: `$link.MacSecConfig.CknSecretIdentifier`, `CakSecretIdentifier`, `Cipher` (`GcmAes128` or `GcmAes256`; the `GcmAesXpn128`/`GcmAesXpn256` ciphers are for ports of 40 Gbps and above, where Microsoft suggests them), optional `SciState`. `Set-AzExpressRoutePort`.
4. Configure the same CKN/CAK and cipher on your router; MACsec runs between your router and the Microsoft MSEE port.

## Gotchas
- Encapsulation (QinQ vs Dot1Q) cannot change later.
- Billing begins when the admin state is enabled on either link.

## Verify
- [ ] `Get-AzExpressRoutePort` shows both links with `AdminState` Enabled.
- [ ] Circuit `ServiceProviderProvisioningState` is `Provisioned` and BGP sessions are up.

## Checked
2026-10-31. Confirmed on Microsoft Learn (ExpressRoute Direct about, ExpressRoute Direct how-to, MACsec how-to): QinQ/Dot1Q fixed at creation, LOA generation with `New-AzExpressRoutePortLOA`, metered circuits at creation, CKN (even length, up to 64 hex) and CAK (32 or 64 hex by cipher) rules, cipher list per port speed, `MacSecConfig` properties, `SciState`, billing starts when a link is enabled. Removed: 2x oversubscription claim, claims about traffic drops when enabling MACsec, IPsec advice, `Get-AzExpressRoutePortLinkConfig`, port-creation billing claim (docs say admin state enabled).
Method: documentation only; no commands were run.
