---
id: computing-software.cloud-infrastructure-engineering.azure.default-outbound-access-retirement-and-private-subnets
name: default-outbound-access-retirement-and-private-subnets
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, default-outbound-access, default-outbound-retirement, private-subnet, defaultoutboundaccess, outbound-connectivity]
level: practitioner
status: docs-checked
description: "Prepare for retirement of Azure default outbound access: find VMs relying on it, mark subnets private, and give workloads an explicit outbound method."
sources: ["https://learn.microsoft.com/azure/virtual-network/ip-services/default-outbound-access", "https://learn.microsoft.com/azure/nat-gateway/nat-overview"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Default outbound access retirement and private subnets

**Goal:** no VM depends on the implicit, Microsoft-owned outbound IP; every subnet is private with an explicit egress path.

## What changes
For the API version released after **31 March 2026**, subnets in new virtual networks have `defaultOutboundAccess` set
to `false` by default: VMs there can't rely on default outbound access and need an explicit method to reach public
endpoints. The change does not alter existing virtual networks, and deployments on earlier API versions keep the earlier
default. The Azure portal already defaults to private subnets.

## Find dependents
- Azure Advisor flags VMs that use default outbound access (open Advisor in the portal).
- Even with a NAT gateway or a UDR to an NVA/firewall configured, a default outbound IP can still be assigned in a
  nonprivate subnet; it is removed only when the subnet is private and the VMs are stopped and deallocated.

## Make a subnet private
```bash
az network vnet subnet update -g rg --vnet-name vnet-app -n snet-app --default-outbound false
```
Existing VMs must be **stopped and deallocated** for the change (private or back to nonprivate) to take effect on their
NICs. Put the explicit method in place first.

## Explicit outbound methods
NAT gateway on the subnet, a UDR to an NVA/firewall, Standard load balancer outbound rules, or an instance-level public
IP. See the outbound-method skill for the trade-offs.

## What breaks on private subnets without explicit egress
Services such as Windows Activation and Windows Updates don't function without an explicit outbound method.

## Gotchas
- Flexible-orchestration scale set instances are secure by default: they have no default outbound IP, so they need an explicit method.
- You can still configure subnets as nonprivate (ARM template, portal, CLI, PowerShell) when a workload isn't ready.

## Verify
- [ ] Subnets show `defaultOutboundAccess` `false` after the change and VMs reach required endpoints via the NAT/firewall IPs.

## Checked
2026-10-31. Confirmed against Learn "Default outbound access in Azure" and the NAT gateway overview: 31 March 2026
API change and its scope, `--default-outbound false`, stop/deallocate requirement, Advisor, Flexible scale sets, Windows
Activation/Updates. Corrected: the retirement date (the skill said 30 September 2025). Removed: Resource Graph query,
the AKS outbound-type advice, NTP and package-repo claims, and the "unreliable" characterisation.
Method: documentation only; no commands were run.
