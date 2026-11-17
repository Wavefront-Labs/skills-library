---
id: computing-software.cloud-infrastructure-engineering.cloud-architecture.architecture-governance-framework
name: architecture-governance-framework
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-architecture
tags: [cloud-architecture, architecture-principles, togaf, architecture-governance-framework, architecture-board, governance-repository, preliminary-phase, decision-rights]
level: practitioner
status: draft
description: "Set up an architecture governance framework in the TOGAF Preliminary phase: decision rights, board charter, processes, compliance, dispensation and the governance log."
sources: ["https://pubs.opengroup.org/togaf-standard/adm/chap02.html", "https://pubs.opengroup.org/togaf-standard/architecture-content/", "https://www.opengroup.org/togaf"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture governance framework setup

## Components (TOGAF governance framework)
- **Process**: policy management, compliance assessment, dispensation, monitoring and reporting,
  business control, environment management.
- **Content**: the governance log - decisions, compliance assessments, dispensations, capability
  assessments, calendar, project portfolio, performance measurement.
- **Context**: who decides (architecture board, design authorities), how escalation works,
  relation to IT governance and change boards.

## Steps
1. **Decision-rights matrix**: list decision types (principle change, new technology, pattern
   deviation, vendor selection, cross-domain interface) and assign decide / consult / inform per
   forum. Push routine decisions to teams with guardrails; reserve the board for cross-cutting.
2. **Board charter**: membership, quorum, cadence, inputs required, SLA for decisions (e.g.
   decision within 10 working days), escalation path.
3. **Processes**: compliance review (when triggered), dispensation (time-boxed, with remediation),
   principle/standard change requests, appeals.
4. **Repository**: where decisions, ADRs, standards and dispensations live; searchable and linked
   to work items.
5. **Measures**: decision lead time, % projects reviewed, dispensations open and overdue, reuse of
   approved patterns.
6. Publish and socialise; review annually.

## Cloud-era adjustments
- Encode as much as possible as automated guardrails (policy-as-code, golden templates) so the board
  only handles exceptions.
- Lightweight ADR review in pull requests for team-level decisions.

## Gotchas
- A board that meets to "approve" every project becomes a bottleneck and gets bypassed.
- No dispensation expiry = permanent exceptions.

## Verify
- [ ] Decision-rights matrix approved by CIO/CTO.
- [ ] Governance log populated for the last quarter with lead-time metrics.
