---
id: business-finance.valuation-and-appraisal.business-valuation.dcf-and-multiples-valuation-with-discounts
name: dcf-and-multiples-valuation-with-discounts
category: business-finance
field: valuation-and-appraisal
product: business-valuation
tags: [business-valuation, company-valuation, dcf, discounted-cash-flow, free-cash-flow, fcff, wacc, terminal-value, gordon-growth, exit-multiple, trading-multiples, comparable-companies, precedent-transactions, ev-ebitda, normalisation, owner-compensation, dlom, dloc, minority-discount, control-premium, purchase-price-allocation, standard-of-value, fair-market-value, valuation-report, sme-valuation]
level: advanced
status: gated
description: "Value a business or stake: standard of value, normalised earnings, DCF with WACC and terminal value, trading and deal multiples, minority and marketability discounts."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# DCF and multiples valuation with discounts

**Goal:** a reasoned value for a company or a shareholding, using an income approach
(DCF) and a market approach (multiples), adjusted for the specific interest being
valued. Credentialed practice (e.g. ASA, CVA/NACVA, CFA, ABV, RICS business valuation)
and reporting standards (IVS, AICPA VS Section 100/SSVS, local equivalents (gated: unconfirmed, source is paywalled or blocked)) govern
formal work; this is the core method.

## 1. Define the engagement
- **Subject:** the whole enterprise, 100% of equity, or a minority stake? Voting or non-voting?
- **Standard of value:** fair market value (hypothetical willing buyer/seller, tax and
  courts), fair value (financial reporting under IFRS 13/ASC 820, or a different
  statutory "fair value" in shareholder disputes — *don't confuse them*), investment
  value (a specific buyer's synergies).
- **Premise:** going concern vs liquidation. **Valuation date**.
These choices alone can move a value by 30%+.

## 2. Normalise the financials
From 3–5 years of accounts, adjust to what a buyer would actually earn:
- **Owner compensation** to market salary for the role (common in owner-managed firms).
- Remove **non-recurring** items (one-off litigation, COVID grants, asset-sale gains).
- **Related-party** rent or transactions to arm's-length terms.
- Non-operating assets (excess cash, investment property) → removed from earnings,
  valued separately and added back.
- Accounting policy differences vs comparables.
Result: normalised EBITDA, EBIT and free cash flow.

## 3. Income approach — DCF
1. Forecast **free cash flow to the firm** for 5–10 years: EBIT × (1 − tax) +
   depreciation − capex − increase in working capital. Tie revenue growth to market
   and capacity, margins to history and peers; challenge management's hockey stick.
2. **Discount rate (WACC):** cost of equity via CAPM (risk-free + beta × equity risk
   premium) plus, for small private firms, size and company-specific premiums (*widely
   used but debated; justify each*); after-tax cost of debt; weights at target or
   market capital structure.
3. **Terminal value:** Gordon growth = FCF₍ₙ₊₁₎ ÷ (WACC − g), with g at or below long-run
   nominal GDP growth; cross-check the implied exit multiple. Terminal value is often
   60–80% of the total (gated: unconfirmed, source is paywalled or blocked) — the key judgement. Check: with WACC 10% and g 3%, the Gordon multiple of next-year FCF is 1/(0.10−0.03) = 14.3 (computed).
4. Mid-year discounting convention if cash flows arrive through the year.
5. Enterprise value → **less net debt** and debt-like items (leases, under-funded
   pensions, deferred revenue where relevant) → plus non-operating assets → equity value.

## 4. Market approach — multiples
- **Guideline public companies:** EV/EBITDA, EV/Revenue, P/E from listed peers; adjust
  for size, growth, margins (small private firms usually warrant lower multiples).
- **Precedent transactions:** multiples paid in acquisitions of similar businesses —
  these typically embed a **control premium** and synergies.
- Apply to normalised metrics consistently (EV multiple × EBITDA → EV, not equity).
- Use the median/interquartile range and explain where the subject sits.

## 5. From enterprise to the interest: discounts and premia
- Multiples from public trading prices give a **marketable minority** basis; transaction
  multiples give **control**.
- **Discount for lack of control (DLOC)** for minority stakes that can't direct dividends,
  sale or management.
- **Discount for lack of marketability (DLOM)** for private shares without a ready market;
  support from restricted-stock and pre-IPO studies or option-based models — magnitudes are
  contested; justify with facts (shareholder agreement, dividend history, exit horizon).
- Apply in the right order and don't double-count (e.g. small-company risk in both the
  discount rate and DLOM).

## 6. Reconcile and report
Compare approaches; weight by data quality (few comparables → lean on DCF; volatile
forecasts → lean on multiples). Run **sensitivity** tables (WACC ±1%, g ±0.5%, margin
±2 pts). The report states scope, standard and premise, sources, normalisations,
assumptions, calculations, discounts with support, conclusion and limiting conditions.
For transactions, a **purchase-price allocation** may follow, splitting price among
tangible assets, identifiable intangibles (customer relationships, brands, technology)
and goodwill under accounting standards.

## Verify
- [ ] Standard of value, premise, subject interest and date are explicit.
- [ ] Each normalisation adjustment listed with evidence.
- [ ] WACC components sourced; terminal growth ≤ long-run nominal growth; implied exit multiple sane.
- [ ] EV-to-equity bridge includes all debt-like and non-operating items.
- [ ] Discounts match the level of value and are not double-counted.
- [ ] Sensitivity range shown alongside the point estimate.
