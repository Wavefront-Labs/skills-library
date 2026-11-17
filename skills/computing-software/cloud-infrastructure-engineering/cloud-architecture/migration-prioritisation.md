---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.migration-prioritisation
name: migration-prioritisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, migration-assessment, migration-prioritisation, wave-candidates, complexity-scoring, business-value-scoring, application-scoring]
level: practitioner
status: draft
description: "Score applications for migration order by business value, complexity, risk and dependencies, producing a defensible priority list that feeds wave planning."
sources: ["https://docs.aws.amazon.com/prescriptive-guidance/latest/application-portfolio-assessment-guide/prioritization.html", "https://learn.microsoft.com/azure/cloud-adoption-framework/plan/prioritize-workloads"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Application migration prioritisation scoring

## Scoring model (example)
| Dimension | Inputs | Weight |
|---|---|---|
| Business value / urgency | DC exit dates, end-of-support, strategic importance | 30% |
| Technical complexity | # servers, OS/DB versions, custom hardware, licence constraints | 25% |
| Dependencies | # inbound/outbound interfaces, latency-sensitive links | 20% |
| Risk | Criticality tier, data sensitivity, compliance | 15% |
| Readiness | Owner engagement, documentation, test availability | 10% |

Score 1-5 per dimension with written definitions; invert complexity/risk so high = easier.

## Steps
1. Pull facts from discovery tools (server counts, utilisation, dependencies) rather than surveys alone.
2. Apply the model in a spreadsheet or the assessment tool; sanity-check outliers with owners.
3. Plot value vs ease: high/high = early waves; low value + hard = retire/retain candidates.
4. Respect hard dependencies: move tightly coupled groups together (move groups).
5. Publish and re-score as discovery improves.

## Gotchas
- Weighting tuned until a favourite app comes first.
- Ignoring end-of-support deadlines that force order regardless of score.

## Verify
- [ ] Every app scored with sources.
- [ ] Owners agreed their app's position.
