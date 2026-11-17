---
id: computing-software.cloud-infrastructure-engineering.azure.platform-landing-zones-connectivity-identity-management
name: platform-landing-zones-connectivity-identity-management
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, platform-landing-zone, connectivity-subscription, management-subscription, identity-subscription, alz]
level: advanced
status: draft
description: "Design the ALZ platform subscriptions: connectivity hub, identity (domain controllers), management (Log Analytics, automation) and their MG placement, RBAC and policy."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/platform-landing-zone", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/network-topology-and-connectivity", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/management", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/identity-access-landing-zones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Platform landing zones: connectivity, identity, management

**Goal:** shared platform services live in dedicated subscriptions under the `Platform` MG,
owned by the platform team, consumed by application landing zones through peering, DNS,
diagnostics and policy.

## MG placement
```
<intermediate-root>
├── Platform
│   ├── Connectivity  → sub-connectivity-prd
│   ├── Identity      → sub-identity-prd
│   └── Management    → sub-management-prd   (+ optional Security for Sentinel)
├── Landing Zones (Corp / Online)
├── Sandbox
└── Decommissioned
```
Separate MGs per platform function let you assign policies specific to each (e.g. identity
denies public IPs and inbound RDP; connectivity allows gateways and firewall public IPs).
Small estates may merge into one platform subscription — CAF allows it, but split RBAC by RG.

## Connectivity subscription
- Hub VNet (or Virtual WAN hub) per region: Azure Firewall, VPN/ExpressRoute gateways, Bastion, DNS Private Resolver.
- **Private DNS zones** for all `privatelink.*` names, linked to hub VNets, centrally (DINE policy creates A records from spokes).
- DDoS Network Protection plan (one per tenant is enough; associate VNets across subs).
- RBAC: NetOps own it; app teams get no write. Spoke peering created by vending pipeline with a scoped identity.

## Identity subscription
- AD DS domain controllers (2+ per region, in zones), or Entra Domain Services.
- Spoke VNet peered to hub; NSGs per DC ports; no public IPs (policy Deny).
- Backup and Update Manager on DCs; Defender for Servers P2.
- Only needed if workloads need Kerberos/LDAP; cloud-native estates can skip it.

## Management subscription
- Central **Log Analytics workspace** (one per region if data residency demands), Automation account if still used, Data Collection Rules, Azure Monitor Agent policy initiatives.
- Sentinel on the same or a dedicated security workspace.
- Workspace retention/commitment tier sized here; all diagnostic settings policies point to it.

## Cross-cutting
- Budgets and alerts per platform subscription; tags `Environment=platform`.
- Platform pipeline identities: Owner on Platform MG, Reader + specific roles elsewhere.
- Break-glass access documented for each platform subscription.

## Gotchas
- Putting firewall and gateways in different subscriptions than the hub VNet is not supported — keep the hub VNet and its appliances together.
- Private DNS zones in multiple subscriptions/regions cause split resolution; one set per tenant (or per sovereign boundary).
- Moving the workspace later breaks every DCR/diagnostic setting — pick the workspace ID early.

## Verify
- [ ] Each platform subscription sits in its MG; `az account management-group show --expand --recurse` matches the diagram.
- [ ] Spoke VNets resolve `privatelink.blob.core.windows.net` via hub resolver.
- [ ] Activity logs from all subscriptions arrive in the management workspace.
