---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.load-based-estimation
name: load-based-estimation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, planning-and-estimating, load-based-estimation, cost-estimation, capacity-planning, cost-model, pricing-calculator]
level: practitioner
status: docs-checked
description: "Estimate cloud cost with the FinOps Planning and Estimating techniques: scenarios, calculators, similar systems, extrapolation, phased builds and trial runs."
sources: ["https://www.finops.org/framework/capabilities/planning-estimating/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Estimating cloud cost

The FinOps Planning and Estimating capability says no single estimating method fits every
situation, so teams need well-understood parameters, scenario planning, tooling and
documentation expectations. Engineering mainly produces estimates, supported by the FinOps team.

## Steps
1. **Define the scenarios** to estimate: the services, architectures or changes, the
   organisation's deployment patterns and the parameters you will need to communicate. The page's
   example compares a virtual machine, a managed service, Kubernetes and serverless for cost,
   effort and impact.
2. **Define scope and the detail required**, then model parameters for the future state.
3. **Choose a technique**, often several together:
   - Cost calculators: good for simple service substitutions, weaker for whole applications or
     environments that do not yet exist in your estate.
   - Similar applications: start from the cost and performance of a comparable system.
   - Extrapolation from past cost: isolate the service changes or usage volumes in an existing
     system; works well for isolated changes in large systems.
   - Future plans: phase the environments (for example development and test first, production
     months later) instead of costing everything at once.
   - Trial run: create the environment from infrastructure as code, run it briefly (the page
     suggests perhaps 1-3 days), then remove it, funding the small cost from R&D or prior
     budget.
4. **Check with FinOps** that estimates follow policy, use appropriate pricing (on-demand,
   discounted rates, expected commitment levels) and include shared costs, platform adjustments,
   support costs, and sustainability or operational impact.
5. **Document the estimate** so it can feed Forecasting and be compared with actuals later.

## Verify
- [ ] The estimate names its scenario, pricing assumptions and included shared costs.
- [ ] It is recorded so a later review can compare it with actual spend.

## Checked

Method: docs-checked 2026-11-09 against the FinOps Planning and Estimating capability page (read through the maturity levels). The provider pricing calculators were not read and were dropped. Removed unconfirmed: the load-driver list, per-unit demand measurement, instance, storage and egress formulas, the worked 2,000 rps example, the easy-to-forget cost lines, sensitivity table and the gotchas.
