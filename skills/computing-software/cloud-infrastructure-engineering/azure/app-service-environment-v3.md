---
id: computing-software.cloud-infrastructure-engineering.azure.app-service-environment-v3
name: app-service-environment-v3
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, app-service-networking, ase, ase-v3, isolated-v2, internal-load-balancer, app-service-environment]
level: advanced
status: docs-checked
description: "Decide on and deploy App Service Environment v3: internal vs external VIP, subnet sizing, Isolated v2 plans, DNS for the ILB domain, zone redundancy and cost."
sources: ["https://learn.microsoft.com/azure/app-service/environment/overview", "https://learn.microsoft.com/azure/app-service/environment/creation", "https://learn.microsoft.com/azure/app-service/environment/networking", "https://learn.microsoft.com/azure/app-service/environment/zone-redundancy"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# App Service Environment v3

**Goal:** single-tenant App Service inside your VNet for workloads that need isolation, very
high scale, or private-only hosting — deployed once correctly because most choices are immutable.

## When ASEv3 (vs multi-tenant + private endpoint + VNet integration)
- Compliance demands single-tenant compute / dedicated hosts (the dedicated host deployment option).
- Very large scale (up to 200 instances total across plans per ASE) or many apps sharing private ingress.
- Need inbound private and outbound fully in VNet without per-app configuration.
Otherwise multi-tenant Premium v3 with PE + VNet integration is cheaper and simpler.

## Network design
- Dedicated subnet, delegated to `Microsoft.Web/hostingEnvironments`, **/24 recommended** (256 addresses); use /23 if you will scale near the 200-instance maximum with frequent scale operations.
- **Internal (ILB)** VIP: private IP in the subnet; default domain `<ase-name>.appserviceenvironment.net`.
- **External**: public VIP; rare now.
- NSG and UDR on the subnet apply; review the networking article for the required outbound dependencies before restricting egress.

## Deploy
```bash
az network vnet subnet create -g rg-net --vnet-name vnet-spoke -n snet-ase --address-prefixes 10.30.0.0/24 \
  --delegations Microsoft.Web/hostingEnvironments
az appservice ase create -g rg -n ase-prod --vnet-name vnet-spoke --subnet snet-ase --kind ASEv3 \
  --virtual-ip-type Internal --zone-redundant true
az appservice plan create -g rg -n asp-orders --app-service-environment ase-prod --sku I1v2 --number-of-workers 3
```
Zone redundancy is chosen at creation; each zone-redundant App Service plan must have at least two instances.

## DNS for ILB
Private DNS zone `ase-prod.appserviceenvironment.net` with:
`*` → ILB IP, `*.scm` → ILB IP, `@` → ILB IP. Link to hub/spoke VNets or forward from on-prem.
Custom domains: CNAME to `<app>.ase-prod.appserviceenvironment.net` plus TLS cert on the app.

## Cost model
See the App Service pricing page and the ASE overview for billing rules (including the charge for an ASE with no instances); prices are not repeated here.

## Gotchas
- Isolated v2 SKUs: I1v2 to I6v2; only I1v2, I2v2 and I3v2 are available on dedicated hosts.

## Verify
- [ ] `az appservice ase show -g rg -n ase-prod` shows the VIP type, kind and zone redundancy.
- [ ] From a peered VNet: app hostname resolves to the ILB IP and serves; no public resolution.

## Checked
2026-10-27. Confirmed on Microsoft Learn: ASE overview, creation and networking articles (/24 recommended, /23 near 200 instances, delegation to
Microsoft.Web/hostingEnvironments, `<name>.appserviceenvironment.net` with `*`, `*.scm` and `@` records, zone-redundant plans need at least two instances,
dedicated host sizes I1v2-I3v2), CLI reference for `az appservice ase` (--kind ASEv3, --virtual-ip-type Internal/External, --zone-redundant) and `az appservice plan`.
Removed: /27 minimum and "can't resize" claim (docs describe moving an ASE to a new subnet), 1-2 hour creation time, no-management-traffic claim,
stamp-fee and empty-ASE billing statements (pricing), memory-optimized SKU claim, scaling-duration claim, `upgradePreference`, internal/external move claim,
`dedicatedHostCount`, and the unconfirmed `--query` property names.

Method: documentation only; no commands were run.
