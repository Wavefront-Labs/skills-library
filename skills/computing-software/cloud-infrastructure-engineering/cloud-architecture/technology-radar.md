---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.technology-radar
name: technology-radar
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, technology-architecture, togaf, technology-radar, technology-standards, service-catalogue, standards-information-base]
level: practitioner
status: draft
description: "Run technology standards as a radar and approved cloud service catalogue: adopt, trial, assess, hold rings, evaluation process and enforcement."
sources: ["https://www.thoughtworks.com/radar/byor", "https://pubs.opengroup.org/togaf-standard/architecture-content/chap05.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/govern/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Technology standards and service catalogue

## Steps
1. **Use radar rings**: Adopt (default choice), Trial (use on real but limited work), Assess
   (explore), Hold (do not start new use). Quadrants: platforms/services, tools, languages
   and frameworks, techniques.
2. **Approved cloud service catalogue**: for each provider service, status (approved,
   approved with conditions, under review, not allowed), conditions (private endpoint
   required, CMK required, regions), owner, landing-zone support.
3. **Evaluation process** for a new service: security review (data handling, IAM model,
   logging, network isolation), compliance attestation scope, cost model, operational
   support, exit path. Target a turnaround of days, not months; slow reviews drive shadow IT.
4. **Enforce lightly**: Azure Policy / SCP / org policy to deny Hold or not-allowed services;
   CI checks on IaC for unapproved resource types.
5. **Publish** the radar quarterly with a short rationale per move.
6. **Sunset Hold items** with migration plans and dates; Hold without a plan accumulates.

## Gotchas
- Allow-listing every new provider service by default is risky; deny-by-default without a fast path is worse.
- Radars that never move anything out of Adopt are inventories, not decisions.

## Verify
- [ ] Every production service type appears in the catalogue with a status.
- [ ] Policy blocks at least the not-allowed list.
