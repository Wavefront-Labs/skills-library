---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.platform-landing-zone
name: platform-landing-zone
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, landing-zone, platform-landing-zone, shared-services, connectivity-subscription, management-subscription, application-landing-zone]
level: practitioner
status: draft
description: "Design the platform landing zone: identity, connectivity, management and security shared services, their ownership, and the contract with application landing zones."
sources: ["https://learn.microsoft.com/azure/cloud-adoption-framework/ready/landing-zone/", "https://docs.aws.amazon.com/prescriptive-guidance/latest/migration-aws-environment/understanding-landing-zones.html", "https://cloud.google.com/architecture/landing-zones"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Platform landing zone and shared services

## Context
CAF splits landing zones into the platform landing zone (centrally run shared services) and
application landing zones (where workloads live). AWS equivalents are the shared accounts under
the Security and Infrastructure OUs; Google uses shared host projects and common folders.

## Steps
1. **Separate platform scopes** by function, each its own subscription/account/project:
   - *Identity*: domain controllers or identity services if needed, federation components.
   - *Connectivity*: hub VNet/Transit Gateway/shared VPC, firewalls, DNS resolvers, private DNS
     zones, on-prem gateways (ExpressRoute/Direct Connect/Interconnect).
   - *Management*: central logging workspace/log archive, monitoring, automation, backup vault
     policies, patch tooling.
   - *Security*: SIEM, security tooling delegated admin (GuardDuty, Defender, SCC), audit.
2. **Ownership**: platform team owns these; application teams never get write access.
3. **Contract with application landing zones**: what the platform provides (peering/attachment,
   DNS, logging, policies, budgets) and what the app team owns. Publish it.
4. **Services delivered by policy**: diagnostic settings, private DNS registration, backup
   policies deployed automatically into application landing zones (DeployIfNotExists, AWS
   Config conformance, org policy).
5. **Scale limits**: check hub limits (peerings per VNet, TGW attachments, routes per table)
   and plan multiple hubs per region.
6. **Deploy as code** with its own pipeline and change process; platform changes affect all.

## Gotchas
- Putting workloads in the connectivity subscription "temporarily" breaks the model.
- Central private DNS zones must be owned by the platform or private endpoint resolution splinters.

## Verify
- [ ] Platform scopes separated with platform-only write access.
- [ ] App landing zone contract published and enforced via policy.
