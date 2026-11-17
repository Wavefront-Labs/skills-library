---
id: computing-software.cloud-infrastructure-engineering.azure.application-security-groups-usage
name: application-security-groups-usage
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nsg, asg, asg-rules, application-security-groups, micro-segmentation]
level: practitioner
status: docs-checked
description: "Use application security groups to write NSG rules by workload role instead of IPs: create ASGs, attach NICs, rule patterns, constraints and limits."
sources: ["https://learn.microsoft.com/azure/virtual-network/application-security-groups", "https://learn.microsoft.com/azure/virtual-network/tutorial-filter-network-traffic", "https://learn.microsoft.com/azure/virtual-network/network-security-groups-overview#application-security-groups"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Application security groups

**Goal:** NSG rules like "web tier may call app tier on 8443" that keep working as VMs are added,
removed or re-IP'd.

## Create and attach
```bash
az network asg create -g rg-app -n asg-web -l westeurope
az network asg create -g rg-app -n asg-api -l westeurope
az network nic ip-config update -g rg-app --nic-name nic-web1 -n ipconfig1 --application-security-groups asg-web
```
## Rules
```bash
az network nsg rule create -g rg-app --nsg-name nsg-snet-app -n Allow-Web-To-Api --priority 1100 \
  --direction Inbound --access Allow --protocol Tcp \
  --source-asgs asg-web --destination-asgs asg-api --destination-port-ranges 8443
az network nsg rule create -g rg-app --nsg-name nsg-snet-app -n Deny-Vnet-To-Api --priority 3000 \
  --direction Inbound --access Deny --protocol '*' \
  --source-address-prefixes VirtualNetwork --destination-asgs asg-api --destination-port-ranges '*'
```
Pattern: allow by ASG pairs, then deny VirtualNetwork to the tier — micro-segmentation inside one subnet.

## Constraints
- All NICs in an ASG must be in the **same VNet**; ASGs in a rule's source and destination must be in the same VNet as each other.
- ASGs can't reference NICs in peered VNets — cross-VNet rules still need prefixes.
- Limits on the Azure subscription limits page: 3,000 ASGs per subscription, 20 ASGs per IP configuration (per NIC), 10 ASGs referenced as source or destination per NSG rule, and 100 ASGs across all rules of one NSG. Check the page for current values.
- A NIC can be a member of several ASGs, up to those limits.

## Operational tips
- Name ASGs by role, not by app owner: `asg-<workload>-<tier>`.
- Assign ASGs in IaC with the VM/NIC so new instances are born segmented.
- An ASG rule affects only NICs that are members; a NIC outside the ASG is unaffected even when the NSG is on its subnet.

## Gotchas
- A NIC in no ASG silently matches nothing — new VMs without the ASG get only default rules → check with Policy/ARG.
- Membership is set on each NIC IP configuration (`--application-security-groups` on `az network nic ip-config update`), so audit it per NIC.

## Verify
- [ ] Each web and api NIC IP configuration shows the intended ASG (`az network nic ip-config show`).
- [ ] Web VM can reach API:8443; a VM outside asg-web cannot.

## Checked

2026-10-31. Confirmed against the Learn application security groups page (rule scoping to member NICs, same-VNet constraints, the allow-then-deny database example), the NSG overview (ASGs as rule source or destination, the AllowVNetInBound default) and the Azure subscription limits page (ASG counts, corrected here: 20 per IP configuration, 10 per rule, 100 per NSG). Removed: the same-region-and-subscription claim, the private endpoint membership claim, the VMSS note, the "asg show doesn't list members" claim and the Resource Graph query (none confirmed). Commands were checked with check_commands.py.

Method: documentation only; no commands were run.
