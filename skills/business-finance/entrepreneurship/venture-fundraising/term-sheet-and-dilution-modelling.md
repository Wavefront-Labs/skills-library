---
id: business-finance.entrepreneurship.venture-fundraising.term-sheet-and-dilution-modelling
name: term-sheet-and-dilution-modelling
category: business-finance
field: entrepreneurship
product: venture-fundraising
tags: [venture-fundraising, entrepreneurship, term-sheet, cap-table, dilution, pre-money, post-money, valuation, safe, post-money-safe, valuation-cap, convertible-note, priced-round, seed-round, series-a, liquidation-preference, participating-preferred, option-pool-shuffle, pro-rata, anti-dilution, broad-based-weighted-average, board-seats, protective-provisions, waterfall]
level: advanced
status: docs-checked
description: "Read a venture term sheet from the founder's side: model pre/post-money dilution, SAFE conversion and the option-pool shuffle, and spot the terms that matter more than headline valuation."
sources: ["https://www.ycombinator.com/documents"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Term sheets and dilution — know what you are actually agreeing to

**Goal:** before signing, model exactly how much of the company each party owns after
the round and what each holder receives at different exit values. Headline valuation is
one term among many, and often not the most important.

## 1. The core arithmetic
- **Post-money = pre-money + new money.** New investor ownership = investment ÷ post-money.
- €2M raised at €8M pre → €10M post → investor owns 20%; existing holders keep 80% of
  what they had.
- **Price per share** = pre-money ÷ fully diluted pre-money shares. "Fully diluted"
  normally counts issued shares, all options (granted and ungranted pool), warrants and
  convertibles — read the definition in the term sheet; it moves the price.

## 2. The option-pool shuffle
Investors often require the pool to be created or topped up **in the pre-money**. That
dilutes only existing holders. Example: €8M pre, €2M raise, investor wants a 15% post-money
pool. The pool (15% of €10M = €1.5M of value) sits inside the €8M, so the founders'
*effective* pre-money is €6.5M. Negotiate the pool size from a hiring plan (who you will
hire in the next 18–24 months and their grants), not a round number.

## 3. SAFEs and convertible notes
- A **post-money SAFE** (the standard Y Combinator form since 2018) fixes the holder's
  ownership: investment ÷ post-money valuation cap. €500k on a €5M post-money cap → 10%
  at conversion, before the priced round's own dilution. Stacking several SAFEs dilutes
  **founders**, not earlier SAFE holders — add them up as you go.
- Pre-money SAFEs and convertible notes convert using a cap and/or discount as their terms say; notes also accrue interest and have a maturity date.
- Model every SAFE/note converting at the next round, then the new money on top.

## 4. Terms that outweigh valuation
- **Liquidation preference** — a founder-friendly baseline is **1x non-participating**: the investor
  takes their money back *or* converts to common, whichever is larger. **Participating**
  preferred ("double dip") or multiples above 1x shift a lot of value in modest exits.
- **Anti-dilution** — *broad-based weighted average* is the milder form; *full ratchet* is harsh.
- **Board composition** — who controls the board after the round? Negotiate the seat count and who appoints the independent explicitly.
- **Protective provisions** — investor vetoes over new shares, sale, debt, budget. Keep them
  to the standard list.
- **Pro-rata rights, information rights, drag-along, no-shop period**.
- **Founder vesting re-set** — investors may ask founders to re-vest; negotiate credit
  for time served.

## 5. Build the cap table and waterfall
Spreadsheet with one row per holder (founders, pool, SAFEs, each round) and columns:
shares before, conversion shares, new shares, shares after, % after. Then a **waterfall**:
for exit values (e.g. €5M, €20M, €100M) compute what each class receives after
preferences. A 1x participating preference looks harmless at €100M and painful at €15M.

Gut-check with a standard tool or your lawyer's model; mistakes in conversion math are common.

## Gotchas
- A higher valuation with a 2x participating preference can leave founders worse off at
  realistic exits than a lower clean valuation.
- "€10M valuation" — ask whether that's pre or post. With SAFEs, post-money caps are the norm.
- Uncapped SAFEs and MFN clauses can surprise you at conversion.
- Over-raising on SAFEs before a priced round is a common source of unexpected founder
  dilution (several 10% SAFEs ≈ 30%+ gone).
- Term sheets are mostly non-binding except confidentiality, no-shop and expenses.
- Jurisdiction matters: SAFE forms are US-centric; UK (ASA, SEIS/EIS considerations) and
  other markets use different instruments. *Confirm with local counsel.*

## Verify
- [ ] Pre-money, post-money, investment and price per share reconcile.
- [ ] Option pool size and whether it's pre- or post-money are explicit; effective pre-money computed.
- [ ] Every SAFE/note converted in the model; founder ownership after the round stated.
- [ ] Liquidation preference type and multiple identified; waterfall run at three exit values.
- [ ] Board composition and protective provisions listed and compared to market standard.

Related: business-finance.entrepreneurship.startup-founding.cofounder-agreement-and-equity-split.

## Checked

Date checked: 2026-10-25. Jurisdiction: General (US-style venture terms); no jurisdiction-specific rule is stated.
Source read: Y Combinator documents page: the post-money SAFE has been the YC standard since 2018; ownership sold is the investment divided by the post-money cap (its example: $500k on a $6.7M cap is about 7.5%). The skill's EUR example (500k on a 5M cap = 10%) follows the same formula.
Arithmetic in the skill (2M at 8M pre = 20%; a 15% pool of 10M post is 1.5M so effective pre-money 6.5M) was recomputed by hand. Removed unconfirmed market-norm claims (liquidation preference "market standard", no-shop length, anti-dilution "standard", board shape, pre-money SAFE conversion rule). Not legal or investment advice; use counsel.

Method: documentation only; no commands were run.
