---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.cost-playbook
name: cost-playbook
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-education, cost-playbook, engineer-guides, cost-best-practices]
level: practitioner
status: draft
description: "Write cost playbooks for engineers: task-based guides per service and pattern, decision tables, commands and links to automation, kept short and current."
sources: ["https://www.finops.org/framework/capabilities/finops-education-enablement/", "https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html", "https://learn.microsoft.com/azure/well-architected/cost-optimization/"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Cost playbooks for engineers

## Structure per playbook
1. **When to use**: trigger (anomaly alert, recommendation ticket, new design).
2. **Decision table**: e.g. storage class by access frequency, instance family by profile,
   serverless vs container by duty cycle, commitment eligibility.
3. **Steps with commands or console paths**, e.g. find unattached volumes:
   `aws ec2 describe-volumes --filters Name=status,Values=available` or Azure Resource Graph
   `Resources | where type == 'microsoft.compute/disks' | where properties.diskState == 'Unattached'`.
4. **Verification**: how to confirm savings (cost dashboard filter, metric to watch).
5. **Risks and rollback.**
6. **Links**: automation, policies, exception process, related playbooks.

## Core set to write first
Responding to a cost anomaly; tagging your resources; rightsizing compute; scheduling
non-production; storage lifecycle and log retention; Kubernetes requests and limits;
reducing data transfer cost; estimating a new design; requesting a commitment or exception.

## Steps
- Write in the engineering portal next to service docs; keep each under two pages.
- Owner and review date on each; update after incidents or provider pricing changes.
- Link playbooks from alerts and recommendation tickets so they are found at the right moment.

## Gotchas
- Generic best-practice lists without commands are not playbooks.
- Pricing figures in playbooks go stale; link to calculators instead of quoting prices.

## Verify
- [ ] Core playbooks published with owners and review dates.
- [ ] Anomaly alerts link to the anomaly playbook.
