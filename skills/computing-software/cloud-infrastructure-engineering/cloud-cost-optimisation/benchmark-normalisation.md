---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.benchmark-normalisation
name: benchmark-normalisation
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-benchmarking, benchmark-normalisation, focus, multi-cloud-comparison]
level: advanced
status: docs-checked
description: "Normalise cost benchmarks across clouds and teams with FOCUS: pick the cost column, treat credits and currency consistently, and document the rules."
sources: ["https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/effectivecost.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/listcost.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/pricingcategory.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/servicecategory.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/contractedcost.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/chargecategory.md", "https://raw.githubusercontent.com/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/v1.2/specification/columns/billingcurrency.md", "https://www.finops.org/framework/capabilities/benchmarking/", "https://www.finops.org/framework/capabilities/data-ingestion/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Normalising benchmarks across clouds

Benchmarks only compare if the data underneath is on one schema and one cost basis. The Data
Ingestion capability says to define the normalisation done between sources, where it is done and
which standards or keys are used; FOCUS is a common way to do it.

## Steps
1. **Common schema.** Convert provider billing data to FOCUS so cost and category columns align.
   Relevant v1.2 columns: `EffectiveCost`, `ListCost`, `ContractedCost`, `ServiceCategory`,
   `PricingCategory`, `ChargeCategory` and `BillingCurrency`.
2. **Choose one cost basis and do not mix.**
   - `EffectiveCost` is the amortised cost after reduced rates, discounts and the applicable
     portion of prepaid purchases; the spec says it is commonly used to track spending trends. The
     original prepaid purchase row is set to 0 because its cost is spread to the eligible charges.
   - `ListCost` (list unit price times quantity) is commonly compared with `ContractedCost`,
     `BilledCost` and `EffectiveCost` to calculate savings from rate optimisation.
   - `ContractedCost` defaults to `ListCost` where no negotiated discount applies.
3. **Credits.** `ChargeCategory` "Credit" covers provider-granted charges such as promotional
   credits, so they can be filtered or footnoted explicitly in a benchmark.
4. **Pricing mix.** `PricingCategory` separates Standard, Committed and Dynamic pricing, which
   helps explain differences between teams that buy differently.
5. **Service comparison.** `ServiceCategory` is the highest-level classification of a service and
   is described as commonly used for analysing costs across providers and tracking workload
   migration.
6. **Currency.** FOCUS costs are denominated in the `BillingCurrency`; aggregate only within one
   currency.
7. **Unit definitions.** Internal benchmarks need clearly defined KPIs and standardised metrics
   across teams and scopes; document the normalisation rules next to each benchmark.

## Gotchas
- The sum of `EffectiveCost` in a billing period may not match the invoices for that period, so do
  not expect a benchmark built on it to tie to invoices.
- Benchmarking should be one component of a broader assessment, not the sole mechanism.

## Checked
Method: docs-checked 2026-11-09 against FOCUS v1.2 column pages (effectivecost, listcost, contractedcost, pricingcategory, servicecategory, chargecategory, billingcurrency) and the FinOps Framework Benchmarking and Data Ingestion pages.
Removed as unconfirmed: the focus.finops.org landing source (no column detail), `RegionId`, `ServiceName` and unit-quantity mapping advice, fixed planning-rate conversion, the rule to exclude support-plan, marketplace and tax lines, and the commitment-strategy gotcha.
