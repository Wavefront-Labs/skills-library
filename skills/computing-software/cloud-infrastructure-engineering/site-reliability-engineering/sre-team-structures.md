---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.sre-team-structures
name: sre-team-structures
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [sre-team-structures, kitchen-sink-sre, embedded-sre-model, infrastructure-sre, consulting-sre, sre-engagement]
level: advanced
status: draft
description: "Choose an SRE team structure (kitchen sink, infrastructure, tools, product/application, embedded, consulting) by org size and need, with pros, cons and when to evolve."
sources: ["https://cloud.google.com/blog/products/devops-sre/how-to-start-and-evolve-your-sre-team", "https://sre.google/workbook/team-lifecycles/", "https://sre.google/workbook/engagement-model/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# SRE team structures

Google Cloud's "SRE team implementations" guidance (and the Workbook's team lifecycle chapter) describe
common structures. Most organisations start with one and evolve.

## Structures
| Model | What it is | Pros | Cons | Fits |
|---|---|---|---|---|
| **Kitchen sink** ("everything SRE") | one SRE team, scope is all services | simple, no gaps, sees cross-cutting patterns | becomes overloaded, shallow; scope creep | first SRE team in a small/medium org |
| **Infrastructure** | SRE owns shared infra (Kubernetes, networking, CI) | high leverage, clear scope | product reliability issues not addressed | orgs with a strong platform layer |
| **Tools** | builds reliability tooling (monitoring, deploy, capacity) | scales via software | risk of building tools nobody adopts | after basics are in place |
| **Product/application** | SRE team per important product area | deep service knowledge, strong partnership | expensive; needs critical mass per team | larger orgs with clear high-value services |
| **Embedded** | SREs sit within dev teams | fast knowledge transfer, influence on design | isolation, inconsistent practices, SRE gets absorbed into dev work | time-boxed engagements, kickstarting practices |
| **Consulting** | SREs advise teams without owning production | broad reach, low cost | limited impact without ownership; context-light | early adoption, spreading practices |

## Evolution path (typical)
1. Kitchen sink team forms; defines SLOs, incident process, on-call for the most critical services.
2. Splits into infrastructure and product-aligned teams as scope grows.
3. Adds consulting/embedded capacity for teams without SRE support; tools work becomes a platform team.

## Design choices regardless of model
- **Ops work cap** (50%) and the mechanism to redirect excess (SRE Book).
- **Engagement model** (PRR, early engagement, frameworks; see `simple-prr-engagement-model`).
- **Staffing**: on-call rotation sizes (see `on-call-schedule-design`) bound minimum team sizes.
- **Mobility**: SREs can move between SRE and dev teams; avoids an ops ghetto.

## Gotchas
- Renaming an ops team to SRE without changing the work (toil cap, engineering time, error budgets)
  changes nothing.
- Embedded SREs need a home SRE team for practice sharing and career growth.

## Verify
- [ ] Documented charter per SRE team: scope, engagement model, ops cap.
- [ ] Reviewed annually against org growth and team load metrics.
