---
id: business-finance.investing-and-trading.venture-capital-private-equity.term-sheet-economics-and-cap-table-waterfall
name: term-sheet-economics-and-cap-table-waterfall
category: business-finance
field: investing-and-trading
product: venture-capital-private-equity
tags: [venture-capital-private-equity, venture-capital, vc, private-equity, term-sheet, pre-money, post-money, valuation, cap-table, capitalisation-table, option-pool, option-pool-shuffle, liquidation-preference, participating-preferred, non-participating, anti-dilution, weighted-average, full-ratchet, pro-rata, safe, convertible-note, valuation-cap, exit-waterfall, preferred-stock, dilution]
level: advanced
status: gated
description: "Read a priced-round term sheet as an investor: pre/post-money and option pool, liquidation preferences, participation, anti-dilution, SAFE conversion, and an exit waterfall."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Term sheet economics and the cap table waterfall

**Goal:** know what each party actually receives at different exit values, before
signing — the headline valuation is only one of several terms that decide that.
Market norms below are typical of US venture practice (NVCA-style documents) at the
time of writing (gated: unconfirmed, source is paywalled or blocked); other markets and later-stage/PE deals differ. **Have counsel review
real documents.**

## 1. Price and ownership
```
post-money  = pre-money + new investment
price/share = pre-money ÷ fully diluted pre-money shares
investor %  = investment ÷ post-money
```
"Fully diluted" includes issued shares, all options granted and the unallocated pool,
warrants, and (usually) converting SAFEs/notes.

**Option pool shuffle:** if the term sheet says the pool (e.g. 10% post-money) must
be created or topped up *in the pre-money*, the dilution falls entirely on existing
holders. Effective pre-money = headline pre-money − value of new pool. Compute it (example: 8M pre, 2M in, post 10M; a 10% post-money pool is 1.0M, so the effective pre-money is 7.0M and the investor still gets 20%).

## 2. SAFEs and convertible notes
YC's standard post-money SAFE comes in three forms (valuation cap only, discount only, MFN); a SAFE carrying both terms is not one of those forms, so read
its conversion clause. For a
post-money cap SAFE, YC says ownership sold equals the investment divided by the post-money cap (500k on 6.7M is about 7.5%), and the
cap is not post the new option pool. That later SAFEs dilute founders rather than earlier SAFE holders is unconfirmed (gated: unconfirmed, source is paywalled or blocked). Model every outstanding instrument converting into the round
— founders are regularly surprised by the stack.

## 3. Liquidation preference (the waterfall's first claim)
- **1× non-participating** (the common norm): on exit, the preferred holder takes the
  **greater of** its money back or its as-converted share (computed: 2M for 20% takes 1M of 1M, 2M of 2M, 2M of 5M, 2M of 10M, 6M of 30M; it converts above 10M).
- **Participating:** takes its money back **and** its pro-rata share of the rest
  ("double dip"); sometimes capped (e.g. at 3×).
- **Multiples > 1×** and **seniority** (later rounds paid first, vs pari passu) matter
  most in low/mid exits.

## 4. Build the exit waterfall
For each exit value (e.g. 10m, 30m, 100m, 300m):
1. Pay debt and transaction costs.
2. Pay liquidation preferences in seniority order.
3. Each non-participating class checks: convert or take preference? (Convert when its
   as-converted share exceeds its preference.) This is circular — iterate, or compute
   breakpoints.
4. Distribute the remainder to common and participating/converted holders pro rata.
Plot payout per class vs exit value. Breakpoints show where incentives diverge (e.g.
founders get nothing below the preference stack — a misalignment for a sale).

## 5. Other economic terms
- **Anti-dilution:** *broad-based weighted average* (norm) adjusts the conversion
  price modestly in a down round; *full ratchet* resets it to the new price — severe.
- **Pro-rata rights:** the right to keep ownership in future rounds.
- **Dividends:** usually non-cumulative "when declared"; cumulative dividends add to
  the preference.
- **Redemption rights, pay-to-play, drag-along** — not economic on day one, decisive
  later.
- Control terms (board seats, protective provisions) are out of scope here.

## Gotchas
- Comparing two offers on headline pre-money while one has a bigger pre-money pool
  or participation.
- Forgetting accrued interest on notes in the conversion.
- Assuming the next round will be priced higher; model a flat and down round too.
- Rounding: carry share counts as integers and prices to several decimals; tie
  the cap table to the company's legal share register.

## Verify
- [ ] Post-money cap table ties: shares × price = post-money; ownership sums to 100%.
- [ ] Option pool placement (pre vs post) and effective pre-money computed.
- [ ] All SAFEs/notes converted with cap vs discount and interest.
- [ ] Waterfall at several exit values with convert-or-preference decisions.
- [ ] Anti-dilution type, participation, multiples and seniority read from the document.
