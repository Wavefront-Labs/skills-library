---
id: business-finance.real-estate-finance.argus.lease-by-lease-model-and-market-leasing-assumptions
name: lease-by-lease-model-and-market-leasing-assumptions
category: business-finance
field: real-estate-finance
product: argus
tags: [argus, argus-enterprise, argus-intelligence, altus-group, real-estate-finance, cre-modelling, lease-by-lease, rent-roll, market-leasing-assumptions, mla, renewal-probability, months-vacant, downtime, free-rent, tenant-improvements, leasing-commissions, recoveries, expense-recovery, general-vacancy, credit-loss, dcf-valuation, exit-cap-rate, scenario-comparison, sensitivity-matrix, audit-trail]
level: practitioner
status: draft
description: "Build a commercial property cash flow in ARGUS: enter leases from the rent roll, set market leasing assumptions for rollover, configure recoveries and vacancy, run the DCF, and audit the output."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# ARGUS lease-by-lease model and market leasing assumptions

**Goal:** produce a commercial property cash flow and valuation in ARGUS (Altus Group)
where every lease, rollover and recovery is explicit, so the output can be audited line by
line and re-run under different market scenarios.

> Product note: this describes ARGUS Enterprise concepts, which carry into Altus's cloud
> successor (ARGUS Intelligence / ARGUS Valuation-DCF modules). Menu names and screen
> layouts differ between versions — **confirm exact navigation in your installed version.**
> The modelling logic is the same.

## 1. Set up the property
- Analysis start date (usually the first of the month after the valuation date), hold
  period (commonly 10 years plus one year so the exit can be priced on forward NOI), area
  measures (rentable vs usable), and currency/units.
- Inflation/growth rates for market rent, expenses and CPI-linked items, by year if needed.

## 2. Enter the rent roll lease by lease
For each tenant: suite and area, lease start and expiry, base rent and **rent steps**
(fixed bumps, % increases, CPI indexation with floors/caps), free-rent periods,
**recovery structure** (gross, net, base-year/expense stop, pro-rata share with caps), any
percentage rent, and the **upon-expiration** behaviour — usually "use market" (apply the
market leasing assumption), or an option with a fixed renewal rent, or vacate.
Model contracted future vacancies (known move-outs) explicitly.

Tie the year-1 base rent total in ARGUS to the rent roll and the T-12 before going further.

## 3. Market leasing assumptions (MLAs) — where the value is decided
Create an MLA profile per space type (e.g. office upper floors, ground-floor retail). Each
blends a **new tenant** and a **renewal tenant** outcome using **renewal probability**:
- Market rent (per area per year), and rent changes over the new term
- Term length
- **Months vacant** (downtime) — applies only to the non-renewing probability share
- Free rent months (new vs renewal)
- Tenant improvements per area (new vs renewal)
- Leasing commissions (% of rent or per area; new vs renewal)
- Recovery structure for the new lease
ARGUS weights the cash flows by the probability: 70% renewal means the rollover shows 30%
of the downtime and a weighted TI/LC — a smooth expected value, not a scenario.

Keep MLAs few and documented; one bespoke MLA per tenant is unreviewable.

## 4. Operating expenses, recoveries and vacancy
- Enter expenses by line (tax, insurance, service charge, utilities, management fee as a %
  of EGI), with growth and whether each is recoverable.
- **General vacancy** and **credit loss** are applied on top of lease-specific downtime — set
  them so you don't double-count (a common option is to reduce general vacancy by
  absorption/turnover vacancy already modelled; *check the setting in your version*).
- Capital items: capex reserves, specific projects, below NOI.

## 5. Valuation
Set discount rate, exit (terminal) cap rate applied to the **year after** the hold's NOI or
NCF, selling costs, and whether to value on NOI or after reserves. Run the DCF; review the
resulting value, implied going-in cap rate and IRR.

## 6. Scenarios and sensitivity
Save scenarios (base, downside market rent, longer downtime) rather than overwriting
assumptions. Use the sensitivity matrix (discount rate × exit cap) for the report.

## 7. Audit the model
- Tenant-level cash-flow report: check a couple of leases month by month around expiry —
  does downtime, free rent, TI and the new rent appear when expected?
- Recoveries report: compare recoveries with the service-charge reconciliation.
- Lease expiration report vs your rollover schedule.

## Gotchas
- Rent entered per month vs per year, or per total vs per area — the biggest single source
  of error. Spot-check one lease's annual rent against the lease.
- Forgetting to set "upon expiration" on leases, so they silently roll at contract rent forever.
- Double-counting vacancy (lease downtime + full general vacancy).
- Exit cap applied to a year that includes a big one-off TI/LC hit.
- Importing a rent roll from Excel without checking date formats.

## Verify
- [ ] Year-1 rent ties to the rent roll and T-12.
- [ ] Every lease has an explicit upon-expiration behaviour.
- [ ] MLAs documented with renewal probability, downtime, free rent, TI and LC (new and renewal).
- [ ] Vacancy not double-counted; recoveries tie to the service-charge reconciliation.
- [ ] Scenarios saved separately; sensitivity matrix produced.

Related: business-finance.real-estate-finance.acquisition-underwriting.rent-roll-to-pro-forma-and-returns.
