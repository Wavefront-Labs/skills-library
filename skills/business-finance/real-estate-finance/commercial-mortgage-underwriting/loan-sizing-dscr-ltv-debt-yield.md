---
id: business-finance.real-estate-finance.commercial-mortgage-underwriting.loan-sizing-dscr-ltv-debt-yield
name: loan-sizing-dscr-ltv-debt-yield
category: business-finance
field: real-estate-finance
product: commercial-mortgage-underwriting
tags: [commercial-mortgage-underwriting, real-estate-finance, cre-lending, loan-sizing, dscr, debt-service-coverage-ratio, ltv, loan-to-value, debt-yield, icr, interest-coverage, mortgage-constant, amortisation, interest-only, underwritten-noi, underwritten-ncf, covenants, cash-sweep, cash-trap, lender-due-diligence, appraisal, refinance-risk, cmbs, balance-sheet-lender]
level: advanced
status: gated
description: "Size a commercial real estate loan as the lender: underwrite NCF, apply DSCR, LTV and debt-yield constraints, take the lowest, then set covenants and check refinance risk at maturity."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Loan sizing with DSCR, LTV and debt yield — how much can this property borrow?

**Goal:** determine the maximum prudent loan against a property by applying each of the
lender's sizing tests to **your own** underwritten cash flow, taking the most restrictive,
then structuring covenants that warn you early if the property weakens.

## 1. Underwrite the lender's cash flow (not the borrower's)
Lenders underwrite conservatively and usually on **in-place** income:
- Contract rents from leases in place (and sometimes only those with a remaining term beyond
  a threshold); no credit for speculative lease-up unless structured (earn-outs, reserves).
- Vacancy at the **higher** of actual and market, often with a floor (e.g. 5%) even for a
  fully let building — *floors vary by lender and asset type*.
- Expenses at the higher of actual, budget and market; a management fee even if self-managed.
- Deduct **replacement reserves, TI and LC** reserves to get **underwritten net cash flow (NCF)**.
Sizing on NCF rather than NOI is common practice (e.g. in CMBS) (gated: unconfirmed, source is paywalled or blocked); know which your credit policy uses.

## 2. The three sizing tests
- **DSCR** = NCF ÷ annual debt service. Max debt service = NCF ÷ required DSCR; max loan =
  max debt service ÷ **mortgage constant** (annual payment per unit of loan, from rate and
  amortisation). Interest-only loans use the rate alone — or a stressed amortising constant.
- **LTV** = loan ÷ appraised value. Max loan = value × max LTV.
- **Debt yield** = NCF ÷ loan. Max loan = NCF ÷ minimum debt yield. Popular because it
  ignores interest rate and cap-rate assumptions — it asks how the lender fares if it owns
  the building.

**Worked example** (illustrative parameters): NCF €1,000,000; required DSCR 1.25×; 6.5%
rate, 30-year amortisation → constant ≈ 7.58% (computed: 12 × monthly payment on 1 at 6.5%/12 over 360 months = 0.075848); value €15.38M (6.5% cap); max LTV 65%;
minimum debt yield 9.5%.
- DSCR: €1,000,000 ÷ 1.25 = €800,000 ÷ 0.07585 ≈ **€10.55M** (computed 10.547M)
- LTV: €15.38M × 0.65 ≈ **€10.00M**
- Debt yield: €1,000,000 ÷ 0.095 ≈ **€10.53M**
→ loan = **€10.0M**, LTV-constrained. Report all three metrics at the final loan amount.

## 3. Rate stress
If the loan is floating rate, size DSCR on the rate plus a cushion or the cap strike rate,
and require an **interest-rate cap or swap**. A loan that only works at today's rate is a
rate bet.

## 4. Structure and covenants
- **Financial covenants:** minimum DSCR/ICR and maximum LTV tested quarterly or annually;
  set headroom between the sizing level and the covenant level (e.g. sized at 1.25×,
  covenant 1.10×) so you get an early warning, not a default on day one.
- **Cash management:** a cash trap or sweep triggered below a DSCR/debt-yield level, before
  the default level; major tenant rollover triggers.
- **Reserves:** tax and insurance escrows, capex, TI/LC, and holdbacks for deferred maintenance.
- **Recourse:** non-recourse with "bad-boy" carve-out guarantees is common in CRE (gated: unconfirmed, source is paywalled or blocked); know what
  your institution requires.

## 5. Lender due diligence checklist
Independent appraisal (instructed by the lender), property condition report, environmental
report (Phase I or local equivalent), title and survey, zoning, insurance review, lease
review and estoppels from major tenants, sponsor track record and liquidity/net worth,
KYC on the borrower and beneficial owners.

## 6. Refinance risk at maturity
Project NCF at maturity and size a hypothetical refinance at a stressed rate and cap rate.
If the loan balance at maturity can't be refinanced on today's terms, you have **maturity
default risk** even if DSCR is fine throughout.

## Gotchas
- Sizing on the borrower's pro forma NOI instead of underwritten in-place NCF.
- A single-tenant building with a lease expiring before loan maturity: the DSCR is binary.
- Appraisal cap rates that lag a moving market.
- Confusing the *interest* rate with the *mortgage constant* in DSCR sizing.
- Ignoring the impact of capex reserves on NCF.

## Verify
- [ ] NCF underwritten independently with vacancy floor, market expenses and reserves.
- [ ] Max loan computed under DSCR, LTV and debt yield; the binding constraint identified.
- [ ] DSCR stressed for rate risk on floating-rate loans; hedge required.
- [ ] Covenant levels have headroom over sizing levels; cash-trap trigger set.
- [ ] Refinance test at maturity performed and documented.

Related: business-finance.real-estate-finance.acquisition-underwriting.rent-roll-to-pro-forma-and-returns.
