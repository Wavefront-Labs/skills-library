---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.dedicated-tenancy
name: dedicated-tenancy
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, deployment-models, dedicated-tenancy, dedicated-hosts, sole-tenant-nodes, azure-dedicated-host, isolated-tenancy, bare-metal]
level: practitioner
status: draft
description: "Decide when dedicated hosts, sole-tenant nodes or isolated tiers are justified (licensing, compliance, noisy neighbours) and design capacity, placement and maintenance for them."
sources: ["https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/dedicated-hosts-overview.html", "https://cloud.google.com/compute/docs/nodes/sole-tenant-nodes", "https://learn.microsoft.com/azure/virtual-machines/dedicated-hosts"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Dedicated hosts and isolated tenancy

## Options
| Option | What you get |
|---|---|
| Dedicated instances (AWS) | Instances on hardware not shared with other customers; no host visibility |
| Dedicated hosts (AWS / Azure) | A whole physical server; socket/core visibility, host affinity, licence tracking |
| Sole-tenant nodes (Google) | Node groups with node affinity labels; CPU overcommit option |
| Bare metal instances | Direct hardware access (no hypervisor), for nested virt or special licensing |
| Isolated PaaS tiers | e.g. App Service Environment, dedicated clusters for managed services |

## Valid reasons
1. **Licensing**: per-socket/per-core licences (Windows Server Datacenter, SQL Server, some Oracle
   terms) that require physical host visibility or licence mobility rules.
2. **Compliance**: a regulator or contract explicitly requiring physical isolation (rarer than
   assumed; most frameworks accept logical isolation with hypervisor assurance).
3. **Performance isolation** for very sensitive workloads.

## Design
- Size host count from instance families supported per host type; plan N+1 host for maintenance
  and failure (a host failure takes all its VMs).
- Use host groups / node groups spread across zones; set auto-placement or affinity rules.
- Enable host recovery / auto-replacement where available.
- Track licence counts per host (AWS License Manager host resource groups).
- Capacity reservations are effectively built in: you pay for the host whether full or empty, so
  bin-pack aggressively.

## Gotchas
- Paying for empty host capacity; monitor host utilisation as a FinOps KPI.
- Not every instance family/size is available on every host type; mixed sizes limit packing.
- Maintenance events move or reboot VMs; read the provider's host maintenance policy.

## Verify
- [ ] Written justification (licence clause or control reference) for each host group.
- [ ] Host utilisation reported monthly; N+1 headroom tested.
