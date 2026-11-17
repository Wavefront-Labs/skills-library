---
id: computing-software.cloud-infrastructure-engineering.azure.avnm-security-admin-rules
name: avnm-security-admin-rules
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, nsg, security-admin-rules, avnm-security, virtual-network-manager, always-allow, network-groups]
level: advanced
status: docs-checked
description: "Enforce organisation-wide network rules with Virtual Network Manager security admin rules: Allow vs Always Allow vs Deny, evaluation order with NSGs, and safe rollout."
sources: ["https://learn.microsoft.com/azure/virtual-network-manager/concept-security-admins", "https://learn.microsoft.com/azure/virtual-network-manager/how-to-block-network-traffic-portal", "https://learn.microsoft.com/azure/virtual-network-manager/concept-enforcement"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Security admin rules via Virtual Network Manager

**Goal:** central security can block high-risk ports everywhere (and guarantee management
traffic) in a way spoke owners' NSGs can't override.

## Evaluation order
1. **Security admin rules** (AVNM) — evaluated first.
   - **Deny**: traffic dropped; NSGs never see it.
   - **Always Allow**: traffic allowed; NSGs are **skipped** for it.
   - **Allow**: traffic passes on to NSG evaluation (NSG can still deny).
2. NSG rules (associated with subnets and NICs).

## Example: block internet-inbound RDP/SSH/SMB org-wide
```bash
az network manager security-admin-config create -g rg-netmgmt --network-manager-name avnm-contoso -n sac-baseline
az network manager security-admin-config rule-collection create -g rg-netmgmt --network-manager-name avnm-contoso \
  --configuration-name sac-baseline -n rc-deny-risky --applies-to-groups network-group-id=<ng-all-vnets>
az network manager security-admin-config rule-collection rule create -g rg-netmgmt --network-manager-name avnm-contoso \
  --configuration-name sac-baseline --rule-collection-name rc-deny-risky -n deny-rdp-ssh-smb-internet \
  --kind Custom --access Deny --direction Inbound --priority 100 --protocol Tcp \
  --sources address-prefix-type=ServiceTag address-prefix=Internet \
  --dest-port-ranges 22 3389 445
az network manager post-commit -g rg-netmgmt --network-manager-name avnm-contoso --commit-type SecurityAdmin \
  --target-locations westeurope --configuration-ids <sac-id>
```
Always Allow example: monitoring/scanner subnet to all VNets on 443/5986 so spoke NSGs can't break it.

## Rollout
- Deploy to one region first and widen: you pick the target regions at each deployment, and the Learn deployments page recommends rolling changes out per region.
- Security admin rules use an eventual-consistency model, so they reach resources shortly after deployment, not instantly.
- Exceptions: put exempt VNets in a separate network group excluded from the rule collection, not per-rule IP holes.

## Gotchas
- Some services have network requirements that deny rules would break. By default AVNM **doesn't apply** security admin rules to a VNet containing Azure SQL Managed Instance or Azure Databricks; setting `AllowRulesOnly` in `securityConfiguration.properties.applyOnNetworkIntentPolicyBasedServices` applies only the Allow rules there.
- Subnets holding Application Gateway, Azure Bastion, Azure Firewall, Route Server, VPN Gateway, Virtual WAN or ExpressRoute Gateway are also skipped; other subnets in the same VNet are covered.
- If several network managers set `applyOnNetworkIntentPolicyBasedServices` differently on one VNet, the manager with the highest scope wins.
- Priority is an integer from 1 to 4,096; the lower the value, the higher the priority.

## Verify
- [ ] The deployment shows status Deployed for the target region on the network manager's Deployment page.
- [ ] RDP from the internet to a test VM whose NSG permits it is dropped.

## Checked

2026-10-31. Confirmed against the Learn pages on security admin rules (actions Allow, Always Allow and Deny, evaluation before NSGs, priority range 1-4,096, services skipped by default, the AllowRulesOnly field and highest-scope rule), on Virtual Network Manager configuration deployments (per-region deployment) and the az network manager CLI reference (commands, flags and post-commit commit types). Removed: the flow-log based rollout and verification steps, the claim that an effective-rules view lists admin rules, the ASE and HDInsight examples and the per-collection priority wording (none are in the docs).

Method: documentation only; no commands were run.
