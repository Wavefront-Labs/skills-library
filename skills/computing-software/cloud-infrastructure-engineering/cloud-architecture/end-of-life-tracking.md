---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.end-of-life-tracking
name: end-of-life-tracking
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-change-management, togaf, end-of-life-tracking, technology-lifecycle, extended-support]
level: practitioner
status: draft
description: "Track technology lifecycle and end-of-support dates for runtimes, databases, OS images and managed service versions, and plan upgrades before forced ones."
sources: ["https://endoflife.date/docs/api", "https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/extended-support.html", "https://learn.microsoft.com/lifecycle/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Technology lifecycle and end-of-support tracking

Providers force upgrades (managed Kubernetes versions, database engine majors, Lambda
runtimes) or charge for extended support (e.g. RDS Extended Support, EKS extended support).
Tracking dates ahead avoids surprise bills and emergency upgrades.

## Steps
1. **Inventory versions** from cloud APIs: engine versions (RDS/Cloud SQL/Azure DB), Kubernetes
   cluster versions, function runtimes, OS images and their AMI/image ages, language
   runtimes from SBOMs or container scans.
2. **Join to lifecycle data**: provider calendars and endoflife.date
   (`https://endoflife.date/api/<product>.json` gives cycles with `eol` and `support` dates).
3. **Classify**: supported, approaching (<12 months), in extended support (paying), out of support.
4. **Plan upgrades** as roadmap items with owners; schedule majors at least 6 months before EOL.
5. **Report** monthly: count and cost of extended-support resources, upcoming EOLs per team.
6. **Prevent**: approved-version policy for new resources; IaC module defaults on current versions.

## Gotchas
- Extended support fees can exceed the instance cost; RDS bills it automatically after standard support ends unless you upgrade.
- Managed service forced upgrades happen on the provider's schedule, sometimes in business hours.

## Verify
- [ ] Dashboard lists every resource with EOL within 12 months and its owner.
- [ ] Extended-support spend tracked and trending down.
