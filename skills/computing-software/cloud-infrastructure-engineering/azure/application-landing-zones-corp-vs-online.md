---
id: computing-software.cloud-infrastructure-engineering.azure.application-landing-zones-corp-vs-online
name: application-landing-zones-corp-vs-online
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, landing-zone, application-landing-zone, corp-landing-zone, online-landing-zone, alz, workload-placement]
level: practitioner
status: draft
description: "Place a workload in the right ALZ application landing zone: Corp (private, hub-connected) vs Online (internet-facing), what policies differ, and how to move between them."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/design-area/application-landing-zone", "https://learn.microsoft.com/azure/cloud-adoption-framework/ready/enterprise-scale/implementation", "https://github.com/Azure/Enterprise-Scale/wiki/ALZ-Policies"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application landing zones: Corp vs Online

**Goal:** each workload subscription lands under the MG whose guardrails fit how it is reached,
so policy helps instead of blocking legitimate designs.

## Decision
| Question | Corp | Online |
|---|---|---|
| Needs to reach on-prem / other spokes privately | yes | optional |
| Serves internet users directly | no (published via hub ingress if at all) | yes |
| Public IPs on workload resources | **Denied** | Allowed (behind WAF) |
| PaaS public network access | Denied, private endpoints required | Allowed where justified |
| Peered to hub | yes, via vending | optional |
Many orgs add MGs like `Confidential-Corp`/`Confidential-Online` (sovereign) or `SAP`; keep
the number of archetypes small — each is a policy set to maintain.

## Corp policy set (ALZ defaults, examples)
- *Deny-Public-Endpoints* for PaaS services (Storage, Key Vault, SQL, Cosmos...).
- *Deny-Public-IP* on NICs, *Deny-MgmtPorts-From-Internet*.
- *Deploy-Private-DNS-Zones* (DINE A records into the hub's privatelink zones).
- *Deny-HybridNetworking* (no gateways in spokes) and subnet must have NSG.

## Online
- WAF-required on App Gateway/Front Door (audit or deny), DDoS on public IP VNets.
- Private endpoints still preferred for data stores even when the front end is public.

## Vending inputs that encode the choice
```hcl
module "lz_vending" {
  source  = "Azure/lz-vending/azurerm"
  subscription_management_group_id = "corp"     # or "online"
  virtual_network_enabled = true
  virtual_networks = { spoke = {
      address_space = ["10.40.0.0/22"], hub_peering_enabled = true,
      hub_network_resource_id = var.hub_vnet_id } }
}
```

## Moving a subscription Corp → Online (or back)
1. Run compliance against the target MG's policy set first (assign the initiative at the sub in `DoNotEnforce`, read results).
2. Move: `az account management-group subscription add --name online --subscription <id>`.
3. Remediate/adjust: Corp → Online may un-peer; Online → Corp requires removing public IPs and adding private endpoints *before* the move or deploys start failing.

## Gotchas
- Deny policies act on next write: existing public resources stay but every update fails — surprises during incident fixes.
- Teams ask for "Online" to avoid private-endpoint work; require an architecture review for Online placement.
- Sandbox MG has no connectivity by design; don't peer sandbox to the hub.

## Verify
- [ ] Workload subscription's MG matches its documented archetype.
- [ ] Policy compliance in the subscription ≥ 95%, exemptions documented.
- [ ] Corp spoke can resolve and reach on-prem; has no public IPs (`resources | where type =~ 'microsoft.network/publicipaddresses' and subscriptionId == '<id>'`).
