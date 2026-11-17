---
id: business-finance.investing-and-trading.securities-trading.order-types-execution-and-position-sizing
name: order-types-execution-and-position-sizing
category: business-finance
field: investing-and-trading
product: securities-trading
tags: [securities-trading, trading, order-types, market-order, limit-order, stop-order, stop-limit, time-in-force, day-order, gtc, ioc, fok, bid-ask-spread, market-microstructure, liquidity, slippage, market-impact, vwap, twap, implementation-shortfall, best-execution, position-sizing, risk-per-trade, stop-loss, gap-risk, auctions]
level: practitioner
status: gated
description: "Execute trades deliberately: pick order type and time-in-force, read spread and depth, measure slippage vs arrival price, size positions by risk, and plan for gaps and auctions."
sources: []
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Order types, execution and position sizing

**Goal:** get in and out of positions at a cost you measured and expected, with a
position size set by how much you're willing to lose, not by how sure you feel.
Exact order behaviour varies by exchange and broker — **check your venue's rulebook
and broker's order-handling disclosure**. Not investment advice.

## 1. Order types (what they guarantee)
| Order | Guarantees | Risk |
|---|---|---|
| **Market** | Execution | Price — fills at whatever is available; dangerous in thin or fast markets |
| **Limit** | Price (or better) | Execution — may not fill |
| **Stop (stop-market)** | Becomes a market order when the stop price trades | Can fill far through the stop on a gap |
| **Stop-limit** | Becomes a limit order at trigger | May never fill if price gaps through |
| **Trailing stop** | Stop that follows price | Same gap risk as stop |
**Time in force:** Day (expires at close), GTC (good-till-cancelled — broker limits
apply), IOC (fill what you can now, cancel the rest), FOK (all now or nothing),
on-open / on-close orders for the auctions.

## 2. Read the market before you send
- **Spread:** bid-ask as % of price. A 0.5% spread is a 0.5% round-trip cost before
  anything moves.
- **Depth:** size at the best bid/offer and a few levels down vs your order. If your
  order is more than a small fraction of displayed size, expect to walk the book.
- **Average daily volume (ADV):** keep an order to a small percentage of ADV
  (single-digit % is a common institutional comfort level — an unsourced heuristic (gated: unconfirmed, source is paywalled or blocked)) or work it
  over time.
- **Time of day:** spreads are often widest just after the open; the **closing
  auction** concentrates liquidity in many markets.
- **Events:** earnings, macro releases and index rebalances change liquidity and gap
  risk.

## 3. Working larger orders
- Slice with a limit price ("marketable limit" a tick or two through the touch caps
  your worst price).
- Algorithms: **VWAP** (track the day's volume profile), **TWAP** (even over time),
  **implementation shortfall / arrival price** (minimise slippage vs decision price,
  trades faster when it can). Choose by urgency vs impact.
- Don't show your full size; avoid predictable patterns (same size, same minute).

## 4. Measure execution
**Implementation shortfall** = (average fill price − decision/arrival price) ×
quantity, plus fees, plus the opportunity cost of unfilled shares. Log every trade:
arrival price, fill, spread at arrival, % of volume. Over time this tells you which
order types and times cost you money.

## 5. Position sizing by risk
```
risk per trade      = account equity × risk %   (e.g. 0.5–1%)
per-share risk      = entry − stop price (+ expected slippage)
position size       = risk per trade ÷ per-share risk
```
Example (computed): 100,000 equity, 0.75% risk, entry 50, stop 47.50 gives 750 ÷ 2.50 = 300 shares.
Then cap by liquidity (% of ADV), concentration (max % of portfolio per position and
per sector), and correlation (five correlated positions = one big position).
Volatility-based stops (e.g. a multiple of average true range) avoid stops that sit
inside normal noise.

## Gotchas
- **Gaps:** overnight or news gaps jump stops; a stop is not a guaranteed loss limit.
  Size for gap risk around events.
- **Market orders in pre-/post-market** or illiquid names can fill shockingly far away.
- **Leverage and margin** turn sizing errors into forced liquidations.
- **Fat fingers:** check quantity vs notional before sending; use broker
  hard limits.
- **Best execution** is a regulatory duty for firms (e.g. MiFID II (gated: unconfirmed, source is paywalled or blocked), FINRA Rule 5310 "Best Execution and Interpositioning", which exists on finra.org) —
  document your order-routing choices if you trade for others.

## Verify
- [ ] Order type and time-in-force chosen for the guarantee you need.
- [ ] Spread, depth and order size vs ADV checked before sending.
- [ ] Position size computed from stop distance and risk %, then capped.
- [ ] Event/gap risk considered for any position held overnight.
- [ ] Trade log records arrival price and implementation shortfall.
