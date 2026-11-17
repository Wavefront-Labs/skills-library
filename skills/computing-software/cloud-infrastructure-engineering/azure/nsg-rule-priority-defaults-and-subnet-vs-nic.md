---
id: computing-software.cloud-infrastructure-engineering.azure.nsg-rule-priority-defaults-and-subnet-vs-nic
name: nsg-rule-priority-defaults-and-subnet-vs-nic
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nsg, nsg-rules, default-rules, rule-priority, network-security-groups, augmented-rules, effective-security-rules]
level: practitioner
status: docs-checked
description: "Design NSG rules: priority numbering scheme, default rules and why they matter, subnet vs NIC evaluation order, augmented rules, stateful behaviour and limits."
sources: ["https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview", "https://learn.microsoft.com/azure/virtual-network/network-security-group-how-it-works", "https://learn.microsoft.com/azure/virtual-network/manage-network-security-group"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# NSG rule priority, default rules, subnet vs NIC

**Goal:** NSGs that are readable, predictable when stacked on subnet and NIC, and easy to extend
without renumbering.

## Default rules (can't delete; priority 65000+)
Inbound: `AllowVNetInBound` (VirtualNetwork→VirtualNetwork), `AllowAzureLoadBalancerInBound`, `DenyAllInBound`.
Outbound: `AllowVnetOutBound`, `AllowInternetOutBound`, `DenyAllOutBound`.
Consequences: everything covered by the `VirtualNetwork` service tag can talk inbound by default (read the service-tag docs for exactly which ranges it covers); internet egress is allowed by default.
To segment, add explicit `Deny VirtualNetwork→VirtualNetwork` at e.g. priority 4000 below your allows.

## Priority scheme
- Range 100–4096, lower first, first match wins.
- Leave gaps: 100–999 platform/security (managed by central team), 1000–2999 workload allows, 3000–3999 workload denies, 4000–4096 catch-all deny.
- Name rules `Allow-Https-From-AppGw` so intent is readable in the portal.

## Subnet vs NIC
- **Inbound**: subnet NSG first, then NIC NSG — both must allow.
- **Outbound**: NIC NSG first, then subnet NSG.
- Intra-subnet traffic is still evaluated (VM to VM in the same subnet passes both NSGs).
- Recommendation: NSG on subnets only; NIC NSGs only for exceptions — two layers double the debugging.

## Augmented rules
Multiple prefixes, ports and service tags/ASGs in one rule:
```bash
az network nsg rule create -g rg --nsg-name nsg-web -n Allow-Web-From-FrontEnds --priority 1000 \
  --direction Inbound --access Allow --protocol Tcp \
  --source-address-prefixes 10.0.1.0/24 10.0.2.0/24 \
  --destination-asgs asg-web --destination-port-ranges 80 443
```
Limits (Azure subscription and service limits page, read 2026-10-27): 2,000 rules per NSG; up to 10 application security groups per rule and 100 across all rules in an NSG.

## Stateful behaviour
Return traffic is allowed automatically; changing a rule doesn't cut existing flows immediately
(existing connections continue until they time out/close).

## Gotchas
- `AzureLoadBalancer` tag is the health probe source (168.63.129.16); denying it marks backends unhealthy.
- Allowing `Internet` inbound to 22/3389 is a common audit finding — use Bastion/JIT.
- Some PaaS subnets (Application Gateway v2, SQL MI, APIM) require specific NSG rules; follow each service's docs.
- Outbound deny-all breaks Azure dependencies (Windows activation, Entra sign-in, updates) unless explicitly allowed; service tags help.

## Verify
- [ ] Effective security rules on a NIC shows the expected merged view.
- [ ] Flow logs (NSG or VNet flow logs) show the expected allowed and denied flows.

## Checked

- 2026-10-27. Confirmed on Microsoft Learn (NSG overview, how NSGs filter traffic, CLI reference for `az network nsg rule`, subscription and service limits): default rule names and priorities 65000/65001/65500, priority range 100-4096, first-match processing, inbound subnet-then-NIC and outbound NIC-then-subnet order, existing connections unaffected by rule changes, rule flags used in the example, 2,000 rules per NSG, ASG limits.
- Removed or corrected: the 1,000 rules and 4,000 IP limits (limits page: 2,000 rules), the Application Gateway port range, KMS port, Front Door service tag in the example, and the claim that flow logs show rule names. Priority bands and subnet-only advice are labelled recommendations.

Method: documentation only; no commands were run.
