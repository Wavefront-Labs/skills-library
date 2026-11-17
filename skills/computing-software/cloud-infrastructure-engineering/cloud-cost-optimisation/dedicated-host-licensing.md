---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.dedicated-host-licensing
name: dedicated-host-licensing
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, licensing-and-saas, dedicated-host-licensing, dedicated-hosts, byol, license-manager, sole-tenant-nodes, windows-server]
level: advanced
status: draft
description: "Use dedicated hosts for licence compliance: when BYOL needs physical cores, AWS Dedicated Hosts with License Manager, Azure Dedicated Host, GCP sole-tenant nodes, and cost maths."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html", "https://docs.aws.amazon.com/license-manager/latest/userguide/host-resource-groups.html", "https://learn.microsoft.com/azure/virtual-machines/dedicated-hosts", "https://cloud.google.com/compute/docs/nodes/bringing-your-own-licenses"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dedicated hosts for licence compliance

Some licences are counted on physical cores or sockets, or forbid running on shared multi-tenant
hardware of certain providers. Dedicated hosts give you the physical server so those licences can
be used.

## When it is needed (verify with your licence agreements)
- **Windows Server / SQL Server BYOL on AWS or GCP** without licence mobility: Microsoft terms after
  1 October 2019 restrict BYOL to "Listed Providers" (AWS, Google, Alibaba) to dedicated hardware
  and to licences acquired before that date or with specific rights; the 2022 Flexible
  Virtualization Benefit excludes Listed Providers. SQL Server with Software Assurance licence
  mobility can run on shared tenancy.
- Per-socket or per-physical-core licences (some Oracle, IBM, legacy ISV software) where counting
  virtual cores is not permitted or is costlier.
- Compliance or isolation requirements.

## Options
- **AWS EC2 Dedicated Hosts**: per-host pricing for a family; visibility of sockets/cores; host
  affinity; **License Manager host resource groups** auto-allocate and release hosts and track
  licence counts. Dedicated Host reservations / savings plans reduce host cost.
- **Azure Dedicated Host**: host groups, fault domains; with Azure Hybrid Benefit, Windows Server
  Datacenter licences cover unlimited VMs on licensed cores.
- **Google Cloud sole-tenant nodes**: node templates and node groups; in-place restart and CPU
  overcommit options to stretch licences.

## Cost maths
```text
host option   = host price (after commitment) + licences you already own (marginal 0 if sunk)
shared option = sum(VM prices) + licence-included uplift per VM
```
Hosts win when packing density is high (many VMs per host) and licences are already owned;
licence-included wins for small or spiky footprints.

## Steps
1. Inventory licences: product, edition, cores, SA/subscription status, purchase date.
2. Determine eligible deployment options per licence.
3. Size hosts by core count needed and packing; plan N+1 for maintenance.
4. Track licence counts against host cores (License Manager rules / SAM tool).

## Gotchas
- Low packing (half-empty hosts) often makes hosts more expensive than licence-included.
- Host maintenance and retirement need spare capacity or host recovery settings.
- Licence terms change; get written confirmation from licensing specialists before migrating.

## Verify
- [ ] Each BYOL workload has documented eligibility and the host or shared choice.
- [ ] Host utilisation (cores used / cores licensed) reported monthly.
