---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.n-tier-architecture
name: n-tier-architecture
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-styles, n-tier, three-tier, layered-architecture, web-tier, app-tier, data-tier, subnet-tiers, lift-and-shift-target]
level: practitioner
status: docs-checked
description: "Lay out a classic N-tier application in the cloud: layers vs tiers, closed and open layers, subnet per tier, load balancers, HA per tier, and when to move to managed services."
sources: ["https://learn.microsoft.com/azure/architecture/guide/architecture-styles/n-tier"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# N-tier architecture

An N-tier architecture divides an application into logical layers and physical tiers (Azure Architecture Center).

## Concepts
- **Layers** separate responsibilities and manage dependencies; a higher layer can use a lower one, not the reverse.
- **Tiers** are physically separate and run on separate machines. Several layers may share a tier.
  Physical separation improves scalability and resiliency but adds network latency.
- **Strict vs relaxed**: in the strict model a request passes through adjacent tiers one by one;
  strict has greater latency and overhead, relaxed has more couplings and harder change. Both can be mixed.
- **Closed layer**: a layer calls only the next layer down. **Open layer**: a layer may call any layer below.
  Closed limits dependencies but can add pass-through network traffic.
- A traditional three-tier app has a presentation tier, an optional middle tier and a database tier.
  Tiers can call each other directly or through a message queue.

## When to use
Evolving architectural requirements; migrating an on-premises app with minimal changes; apps spanning
on-premises and cloud. Use VMs when migrating with minimal refactoring; otherwise prefer managed
services such as App Service or Container Apps.

## Layout on VMs (Azure reference)
1. Each tier is a virtual machine scale set with two or more VMs; a load balancer fronts each tier;
   scale a tier horizontally by adding VMs.
2. Each tier gets its own subnet so network security group rules and route tables apply per tier.
3. Web and business tiers stateless (any VM serves any request). Data tier is a replicated database,
   managed where possible; SQL Server Always On availability groups on Windows, or a replicating
   database such as Apache Cassandra on Linux.
4. NSGs restrict each tier; the data tier accepts requests from the business tier only.
5. Optional perimeter network (DMZ) with network virtual appliances, two or more in a scale set behind
   an external load balancer. Place a WAF between front end and internet.
6. Block direct RDP and SSH to application VMs; use Azure Bastion over private IPs.
7. Use autoscaling, asynchronous messaging to decouple tiers, and caching for data that rarely changes.
   Consider layer-7 routing when there are more than three tiers.

## Challenges (page list)
- A middle tier that only does CRUD adds latency and complexity without value.
- Monolithic design prevents independent deployment of features.
- Network security is harder to manage in large systems.
- Requests crossing many tiers make testing and monitoring harder.

## Verify
- [ ] Each tier has 2+ instances behind a load balancer and its own subnet and access rules.
- [ ] Only the middle tier can reach the database tier.

## Checked
Confirmed against the Azure n-tier page. The cited AWS web hosting whitepaper was not fetched and
is dropped, as are claims that depended on it.
Method: docs-only read of cited pages, 2026-11-08
