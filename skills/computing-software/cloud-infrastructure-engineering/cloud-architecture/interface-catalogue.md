---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.interface-catalogue
name: interface-catalogue
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, information-systems-architecture, interface-catalogue, togaf, phase-c, application-communication-diagram, integration-inventory]
level: practitioner
status: draft
description: "Build an application communication diagram and interface catalogue: every interface with protocol, data, direction, volume, criticality and owner, ready for migration."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap06.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap04.html", "https://docs.aws.amazon.com/prescriptive-guidance/latest/application-portfolio-assessment-guide/introduction.html"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application communication diagram and interface catalogue

## Steps
1. **Discover interfaces** from several sources: architecture docs, integration platform
   configs (ESB, MFT, API gateway), firewall rules, network flow logs or dependency mapping
   tools, batch schedulers, and interviews. Flow data catches what documentation forgot.
2. **Catalogue each interface**: ID, source, target, direction, pattern (sync API, message,
   file transfer, DB link, shared database), protocol and port, data entities carried,
   frequency/volume, latency tolerance, security (auth, encryption), owner, criticality.
3. **Draw the application communication diagram** per domain from the catalogue (generate it
   if your EA tool can) instead of hand-maintaining a picture.
4. **Flag migration risks**: hard-coded IPs, DB links and shared databases, chatty sync calls
   across future venue boundaries, file drops on shared drives, mainframe dependencies.
5. **Use it for move groups**: interfaces with low latency tolerance keep systems together.
6. **Keep it live**: update via change process; reconcile against flow logs quarterly.

## Gotchas
- Shared-database "interfaces" are invisible in API inventories and break migrations.
- Undocumented month-end or year-end batch feeds surface only with long flow-log windows.

## Verify
- [ ] Catalogue reconciled against at least 30 days of flow data.
- [ ] Each interface has an owner and criticality.
