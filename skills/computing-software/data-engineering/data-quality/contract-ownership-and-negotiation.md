---
id: computing-software.data-engineering.data-quality.contract-ownership-and-negotiation
name: contract-ownership-and-negotiation
category: computing-software
field: data-engineering
product: data-quality
tags: [data-quality, contract-negotiation, data-contracts, ownership, governance]
level: advanced
status: draft
description: "Establish data contract ownership and negotiate terms between producers and consumers: who owns what, change requests, SLAs, versioning commitments and escalation."
sources:
  - https://bitol-io.github.io/open-data-contract-standard/latest/
  - https://datacontract.com/
  - https://www.oreilly.com/library/view/data-contracts/9781098157623/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Contract ownership and negotiation

**Goal:** contracts that both sides agreed to and maintain, rather than documents imposed by consumers and ignored by producers.

## Roles
- **Producer (owner)**: the team that generates the data; owns the contract, its schema and guarantees, and changes to it.
- **Consumers**: register as dependents; can request changes and must be notified of breaking changes.
- **Platform/governance**: provides tooling, templates, registry, enforcement; arbitrates disputes.

## What gets negotiated
- Schema and semantics (definitions of each field, units, nullability).
- Quality rules and thresholds (what the producer guarantees vs what consumers check themselves).
- SLAs: freshness, availability, support hours, incident response.
- Change policy: notice period for breaking changes (e.g. 30-90 days), versioning (v1/v2 side by side), deprecation windows.
- Access and privacy: classification, permitted uses.

## Process
1. Consumer raises a request (new dataset, new field, stronger guarantee) with the business reason.
2. Producer assesses cost/feasibility; proposes terms.
3. Agree and record in the contract file (ODCS/YAML in the producer's repo), reviewed in a PR by both sides.
4. Enforcement wired in CI and runtime checks.
5. Review periodically or on incidents.

## Practical rules
- Start with the minimum consumers actually need; every guarantee costs the producer.
- Not every dataset needs a contract: prioritise cross-team, business-critical interfaces.
- Contracts change through PRs with consumer reviewers; no silent edits.
- Escalation path for unresolved disputes (data governance council or domain leads).

## Gotchas
- Contracts written by the data team on behalf of producers have no owner and rot.
- Unbounded consumer lists make every change a negotiation: register consumers explicitly so impact is known.

## Verify
Each contract has a named producer owner, registered consumers, an agreed change policy, and PR history showing both sides approved.
