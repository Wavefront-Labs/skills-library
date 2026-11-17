---
id: computing-software.cybersecurity-defensive.threat-modelling.trike-threat-modelling
name: trike-threat-modelling
category: computing-software
field: cybersecurity-defensive
product: threat-modelling
tags: [trike, requirements-model, actor-asset-action-matrix, threat-modelling, risk-based]
level: advanced
status: gated
description: "Apply the Trike methodology: build the actor-asset-action requirements matrix, derive threats as elevation of privilege or denial of service, and assign risk to each."
sources: ["https://www.octotrike.org/", "https://www.octotrike.org/papers/Trike_v1_Methodology_Document-draft.pdf", "https://insights.sei.cmu.edu/blog/threat-modeling-12-available-methods/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Trike threat modelling

Trike starts from a **requirements model** of who may do what to which asset,
then treats any deviation from that model as a threat. It suits systems where the authorisation model is the
core risk (multi-tenant SaaS, back-office tools).

## 1. Requirements model: the actor-asset-action matrix
- **Actors**: roles that interact with the system (anonymous, customer, support, admin, partner API).
- **Assets**: data or resources the system manages (accounts, orders, invoices).
- **Actions**: CRUD (create, read, update, delete) per asset.
- For each cell, state whether the actor is **allowed, disallowed, or allowed under rules** (e.g. "customer
  may read order only if they own it"). Rules are the business logic to verify.

| Asset / Action | Customer | Support | Admin |
|---|---|---|---|
| Order: Read | own only | any, logged | any |
| Order: Update | own, status=draft | address only | any |
| Order: Delete | never | never | soft delete |

## 2. Implementation model
A DFD of the actual system with trust boundaries, showing which processes handle each action. Use cases are
walked through the DFD to confirm every allowed action has a path.

## 3. Threat generation
Trike defines threats mechanically from the matrix:
- **Elevation of privilege**: any actor performing a disallowed action, or an allowed action outside its rules.
- **Denial of service**: an allowed actor prevented from performing an allowed action.
Every cell therefore yields candidate threats, which are then traced through the DFD to find where they could
occur (missing check, confused deputy, IDOR).

## 4. Risk model
Per the SEI survey of methods, Trike rates each CRUD action on a five-point probability scale, rates actors on
five-point risk scales, and evaluates each actor action on an always/sometimes/never scale. Each threat becomes
the root node of an attack tree. Most teams use a simpler ordinal scale.

## Gotchas
- The methodology documentation is a draft and tooling is dated (gated: unconfirmed, source is paywalled or blocked); teams take the matrix and threat-generation
  ideas and skip the rest.
- The matrix grows fast; group assets with identical rules.
- Rules in cells must be testable statements; vague rules hide bugs.

## Verify
Each "disallowed" and "rules" cell has a corresponding authorisation test (unit or DAST), and each threat maps
to a DFD element where its check is enforced.

## Checked
2026-10-28. Confirmed in the SEI blog threat-modeling-12-available-methods: requirements model with actors, assets, intended actions and rules; actor-asset-action matrix with CRUD cells valued allowed, disallowed or action with rules; DFD mapped to actors and assets; threats are elevation of privilege or denial of service; five-point and always/sometimes/never risk scales. Removed: author names and year, the claim about original tooling. The draft status of the methodology document is gated because octotrike.org returned 403.
Method: documentation only; no commands were run.
