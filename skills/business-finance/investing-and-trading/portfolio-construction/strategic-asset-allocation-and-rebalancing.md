---
id: business-finance.investing-and-trading.portfolio-construction.strategic-asset-allocation-and-rebalancing
name: strategic-asset-allocation-and-rebalancing
category: business-finance
field: investing-and-trading
product: portfolio-construction
tags: [portfolio-construction, asset-allocation, strategic-asset-allocation, saa, tactical-asset-allocation, diversification, correlation, rebalancing, rebalancing-bands, calendar-rebalancing, risk-budgeting, volatility, drawdown, policy-portfolio, investment-policy-statement, ips, benchmark, performance-attribution, brinson, mandate-constraints, mean-variance, 60-40]
level: practitioner
status: gated
description: "Set a strategic asset allocation from objectives and constraints, size risk not just weights, rebalance with bands, and attribute performance to allocation vs selection."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Strategic asset allocation and rebalancing

**Goal:** a written policy portfolio that matches the investor's return need, risk
tolerance and constraints, kept on target with a rebalancing rule rather than
discretion, and measured against a benchmark that reflects the policy. Asset
allocation explains most of the variability of a diversified portfolio's returns over
time (gated: unconfirmed, source is paywalled or blocked) — get it right before picking securities. Not personal advice; numbers below
are illustrative.

## 1. Objectives and constraints (write them in an IPS)
- **Return objective** (e.g. CPI + 4% over rolling 10 years) and **risk tolerance**
  (maximum acceptable drawdown, volatility, probability of shortfall).
- **Constraints:** time horizon, liquidity needs (cash outflows in the next 1–3 years),
  tax, legal/regulatory (mandate limits, prohibited assets), unique preferences (ESG
  exclusions).
- Governance: who decides, who rebalances, how often reviewed.

## 2. Build the allocation
1. Choose **asset classes** that are distinct (low correlation), investable and
   liquid enough: e.g. domestic equity, global equity, government bonds, credit,
   inflation-linked bonds, real assets, cash.
2. Set **capital market assumptions**: expected return, volatility and correlations
   per class, with a stated source and date. These drive everything — treat them as
   uncertain.
3. Candidate allocations: mean-variance optimisation (with constraints, because
   unconstrained optimisers produce extreme, unstable weights), or simpler
   heuristics (e.g. 60/40, risk parity, a reference portfolio).
4. **Check risk, not just weights:** a 60/40 equity/bond portfolio typically gets
   ~90% of its volatility from equities (computed with assumed volatilities: 16%/5% and correlation 0 gives 96%; 16%/6% and 0.2 gives 90%; 15%/5% and 0.3 gives 90%; so the share depends on the inputs). Report each class's contribution to risk.
5. **Stress test** against historical episodes (2008, 2020, 2022's joint stock-bond
   fall) and the investor's liabilities or spending needs.

## 3. Rebalancing
- **Calendar** (quarterly/annually) is simple; **bands** react to markets. A common
  hybrid: check monthly, trade only when a class drifts outside its band.
- Band sizing: wider for volatile, expensive-to-trade or illiquid classes. A typical
  form is ±5 percentage points absolute or ±20–25% relative to target, whichever is
  tighter (heuristic; not a standard).
- Rebalance **to target or to the band edge**: to the edge trades less.
- Use **cash flows first** (contributions, withdrawals, dividends) to rebalance before
  selling — cheaper and often tax-free.
- In taxable accounts, account for realised gains; rebalance within tax-advantaged
  accounts where possible.

## 4. Measure
- **Policy benchmark** = target weights × asset-class index returns.
- **Brinson-style attribution:** total active return = allocation effect (over/under-
  weighting classes) + selection effect (beating each class's index) + interaction.
- Review the policy itself every 3–5 years or on a change in circumstances — not after
  a bad quarter.

## Gotchas
- **Correlations rise in crises**; diversification you measured in calm markets
  shrinks when you need it.
- **Home bias** concentrates risk in one economy and currency.
- **Illiquid assets** (private equity, property) look low-volatility because they're
  rarely revalued (smoothed returns) — understates true risk.
- **Currency:** decide hedging policy per class; unhedged foreign bonds behave like a
  currency bet.
- Rebalancing "feels wrong" (buying what fell) — that's why the rule must be written
  in advance.

## Verify
- [ ] IPS states return objective, risk limits, constraints and governance.
- [ ] Capital market assumptions sourced and dated.
- [ ] Risk contribution by class reported, not just weights.
- [ ] Rebalancing rule (frequency, bands, to-target or edge) written and followed.
- [ ] Performance compared to the policy benchmark with allocation vs selection split.
