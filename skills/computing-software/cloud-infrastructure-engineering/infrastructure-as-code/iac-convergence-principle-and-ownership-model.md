---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.iac-convergence-principle-and-ownership-model
name: iac-convergence-principle-and-ownership-model
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-fundamentals, convergence-principle, infra-ownership-model, idempotency]
level: practitioner
status: draft
description: "Apply convergence and idempotence as IaC design principles and define who owns which infrastructure code: platform team, product teams, shared modules and on-call."
sources: ["AWS Well-Architected Operational Excellence - infrastructure as code (https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/welcome.html)", "Google Cloud Architecture Framework - infrastructure as code (https://cloud.google.com/architecture/framework)", "Team Topologies - platform teams (https://teamtopologies.com/key-concepts)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Convergence and ownership in IaC

## Convergence and idempotence
- **Idempotent**: applying the same code twice changes nothing the second time.
- **Convergent**: from any starting state (fresh, partly configured, drifted) applying the code reaches the declared state.
Convergence is the stronger property and the real goal: it is what makes reruns safe after failures and what makes drift remediation possible.

Design rules:
1. Declare end state, not steps (`state: present`, Terraform resources) — avoid scripts that assume a starting point.
2. Every imperative step needs a guard (creates/removes, `changed_when`, `count` conditions).
3. Partial failure must be re-runnable: no "run once" steps without markers.
4. Test convergence explicitly: run on a fresh host, a converged host (expect zero changes), and a deliberately drifted host (expect only the drift corrected).
5. Ordering dependencies are explicit (handlers, `depends_on`), never accidental.

## Ownership model
| Layer | Typical owner | Notes |
|---|---|---|
| Landing zone, networks, identity, org policies | platform/cloud team | high blast radius, strict review |
| Shared modules/roles/collections | platform team with contribution model | versioned, documented interfaces |
| Service infrastructure (app DBs, queues, app hosts) | product teams | consume shared modules |
| Automation platform (AAP, CI runners) | platform team | SLOs, upgrades |

Make ownership machine-readable:
- `CODEOWNERS` per directory/stack.
- Repo or stack metadata (owner, on-call, cost centre) as tags/labels.
- One owner per state file / inventory scope; shared state with many writers is an incident waiting.

## Gotchas
- "Everyone can change everything" repos make reviews meaningless; split by ownership boundary.
- A platform team owning every change becomes a bottleneck: publish modules and let product teams self-serve within policy.

## Verify
- [ ] Every stack/inventory has a named owner and a convergence test (fresh + rerun + drifted).
