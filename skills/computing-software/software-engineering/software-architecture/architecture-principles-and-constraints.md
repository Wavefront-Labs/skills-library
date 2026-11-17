---
id: computing-software.software-engineering.software-architecture.architecture-principles-and-constraints
name: architecture-principles-and-constraints
category: computing-software
field: software-engineering
product: software-architecture
tags: [software-architecture, architecture-description, architecture-principles, constraints, togaf-principles, guardrails]
level: practitioner
status: draft
description: "Write architecture principles (statement, rationale, implications) and record constraints, then enforce them with fitness functions and review instead of slideware."
sources: ["https://pubs.opengroup.org/togaf-standard/adm-techniques/chap02.html", "https://docs.arc42.org/section-2/", "https://www.thoughtworks.com/insights/articles/fitness-function-driven-development"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Architecture principles and constraints

## Principles vs constraints
- **Constraint**: imposed, non-negotiable (regulation, existing contract, mandated cloud, team
  skills, budget, deadline). Record in arc42 section 2 with source.
- **Principle**: a chosen rule that guides many decisions, which you could have chosen differently.

## Writing a principle (TOGAF format)
```
Name:        Data has one owner
Statement:   Every business entity is created and changed by exactly one service; others consume
             copies via events or APIs.
Rationale:   Shared writable data couples teams' release cycles and corrupts invariants.
Implications: No shared write tables; services publish change events; reporting uses a separate
             analytical store; existing shared tables get an owner within 2 quarters.
```
Good principles are few (5-10), specific enough to rule something out, and have implications that
cost something. "Use best practices" or "be scalable" rule nothing out.

## Examples that work
- Prefer managed services over self-hosted unless a written exception (ADR).
- APIs are designed contract-first and versioned; no breaking change without new version.
- Everything deployable from source via pipeline; no manual production changes.
- Personal data stays in-region (constraint from GDPR/contract, enforced by principle).

## Make them real
- Map each principle to enforcement: architecture fitness functions (ArchUnit rules, dependency-cruiser,
  policy-as-code with OPA/Conftest on Terraform), templates/golden paths, and review checklists.
- Exceptions go through an ADR with expiry date.
- Revisit yearly; delete principles nobody can cite a decision for.
