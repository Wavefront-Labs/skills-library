---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.finops-scopes
name: finops-scopes
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, finops-principles, finops-scopes, finops-framework, saas-scope, data-center-scope, ai-scope, technology-spend, finops-scope-onboarding]
level: practitioner
status: docs-checked
description: "Define FinOps Scopes per the FinOps Framework: segments of spend tied to a business decision, which personas, capabilities and domains apply, and when to retire one."
sources: ["https://www.finops.org/framework/scopes/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# FinOps scopes

## What a scope is
A FinOps Scope is a defined segment of spending across technology categories, aligned to business constructs such as
product, cost center or environment. It sets the decision context for a FinOps practice and determines which Personas are
engaged, which Capabilities are applied and which Domains define success. A practice typically defines several scopes.

## Define a scope
1. Start from an explicit business question, usually from leadership (for example "what are we spending on AI?"). Use the
   Five whys to find the decision and outcome behind it.
2. Check whether an existing scope already supports that decision. Create a new one only when a distinct business outcome,
   constraint or decision context needs it; keep scopes few, simple and purposeful.
3. For the scope, choose intentionally which Personas, Capabilities and Domains apply. Capabilities stay common across
   scopes, but inputs, KPIs, maturity and success measures can vary. Considerations include how often each capability is
   performed, how strictly governance is applied, expected KPI levels and how broad optimisation is.
4. Revisit the profile as the practice evolves.

## Principles from the page
- Scopes reflect decision context, not infrastructure boundaries; one scope may span several products, cost centers or
  environments, and several scopes may exist inside one area of spend.
- Scopes can extend beyond public cloud (the page discusses AI, SaaS and data center material) and are driven by the
  business, not the technology.
- Scopes are situational: when the outcome is achieved or no longer relevant, let the supporting activity fade.
- Scopes are not always mutually exclusive. Where usage sits in two scopes with different expectations (for example
  accurate cloud forecasting and experimental AI spend), decide whether to exclude it from one or keep it and account for
  its effect on forecast variance.

## Gotchas
- Creating a scope because a topic is interesting rather than because the business wants to influence a decision.
- Many scopes add overhead.

## Verify
- [ ] Each scope names the business question or outcome that justifies it.
- [ ] Overlaps between scopes are explicit, with how each affects the other's targets.

## Checked
Confirmed against the FinOps Foundation Framework "FinOps Scopes" page: definition, role of personas, capabilities and
domains, creation criteria, Five whys technique, decision context versus infrastructure, lifecycle, overlap handling.
Removed: the per-scope capability priority table, scope examples with named personas and data sources, the maturity
target advice (crawl for SaaS), the FOCUS normalisation claim, the "2025 update" statement and the two other sources
(not read this batch).
Method: docs-checked 2026-11-09 against https://www.finops.org/framework/scopes/
