---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.well-architected-review
name: well-architected-review
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, operational-excellence, well-architected-review, well-architected-tool, architecture-review, improvement-plan]
level: practitioner
status: draft
description: "Run a Well-Architected review: scope a workload, use the WA tool and lenses, identify high-risk issues, build an improvement plan and repeat milestones."
sources: ["https://docs.aws.amazon.com/wellarchitected/latest/userguide/intro.html", "https://learn.microsoft.com/assessments/azure-architecture-review/", "https://cloud.google.com/architecture/framework"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Well-Architected review process

## Steps
1. **Scope one workload** (not an account): its owner, architecture, business context and criticality.
2. **Tooling**: AWS Well-Architected Tool (pillar questions, lenses such as Serverless, SaaS,
   Generative AI, custom lenses), Azure Well-Architected Review assessment, Google Cloud
   Architecture Framework checklists.
3. **Participants**: workload team (architect, lead engineer, ops), a facilitator who is not on
   the team, security and FinOps for their pillars. 2-4 hours, or split by pillar.
4. **Answer honestly** against best practices; mark not applicable with reason. The tool flags
   **high-risk issues (HRIs)** and medium risks.
5. **Prioritise**: HRIs on tier-1 workloads first; pick a handful of improvements per
   quarter rather than the whole list.
6. **Improvement plan**: backlog items with owners and dates; link to the review.
7. **Milestones**: save a milestone after the review and after improvements; re-review annually
   or after major change; track HRI count over time.
8. **Aggregate** across workloads to find systemic issues best fixed centrally (landing zone, templates).

## Gotchas
- Reviews as audits create defensive answers; frame as a learning exercise.
- Improvement plans not in the team's backlog never happen.

## Verify
- [ ] HRIs for tier-1 workloads trending down across milestones.
- [ ] Improvement items in team backlogs with owners.
