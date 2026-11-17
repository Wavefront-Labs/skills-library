---
id: sports-recreation.gambling-and-wagering.betting-exchange-trading.back-lay-liability-and-greening-up
name: back-lay-liability-and-greening-up
category: sports-recreation
field: gambling-and-wagering
product: betting-exchange-trading
tags: [gambling-and-wagering, betting-exchange-trading, betting-exchange, betfair, smarkets, matchbook, back, lay, lay-bet, liability, commission, market-base-rate, green-up, hedge, cash-out, scalping, swing-trading, pre-race-trading, in-play, ladder, liquidity, matched, unmatched, keep-bet, courtsiding, latency, trading-software, responsible-gambling]
level: practitioner
status: draft
description: "Betting exchange trading: how backing and laying work, lay liability, commission, calculating a hedge to green up equal profit, and pre-race and in-play trading risks."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Betting exchange trading — back, lay, liability and greening up

**Goal:** use an exchange (Betfair, Smarkets, Matchbook-style) correctly:
know your liability on every lay, calculate a hedge that locks in equal
profit, and understand why most "traders" lose. **Draft; commission rates
and features differ by exchange and country.**

## 1. Back vs lay
- **Back** = bet that something happens (like a bookmaker bet).
- **Lay** = bet that it does *not* happen — you act as the bookmaker.
- **Lay liability = lay stake × (odds − 1).** Laying £10 at 5.0 risks
  £40; you win £10 (minus commission) if the selection loses.
- Laying at long odds creates large liabilities for small wins — check the
  liability figure, not the stake, before confirming.

## 2. Commission and matching
- Exchanges charge **commission on net winnings per market** (commonly a
  few percent; varies by exchange, account and promotions). Losing
  markets pay none.
- Your bet is **matched** only when someone takes the other side.
  Unmatched bets can be cancelled, or set to persist/"keep" in-play.
- Liquidity: thin markets have wide gaps between best back and lay prices;
  trading them is expensive.

## 3. Greening up (hedging to equal profit)
You backed £10 at 4.0; the price shortens to 3.0. To lock in equal profit:
`lay stake = back stake × back odds / lay odds = 10 × 4.0 / 3.0 = £13.33`
- If it wins: +£30 back profit − £26.67 lay liability = **+£3.33**.
- If it loses: −£10 back stake + £13.33 lay win = **+£3.33**.
(Before commission.) Same formula reversed for lay-first positions:
`back stake = lay stake × lay odds / back odds`.
Reverse case (price drifts) gives equal **red** (loss) — "redding up"
limits the loss. Most exchanges/apps have a one-click cash-out/hedge.

## 4. Styles
- **Pre-race / pre-match trading:** take positions on price movement
  before the event (e.g. horse racing in the final minutes when liquidity
  peaks). Requires reading the ladder, weight of money (often misleading)
  and news.
- **Scalping:** many tiny trades of 1–2 ticks in very liquid markets.
  Small edges, eaten by commission and mistakes.
- **Swing trading:** larger moves based on expected price direction.
- **In-play:** prices move fast on events; you compete against faster data
  feeds and courtsiders. Exchanges apply **in-play delays** to bet placement.

## 5. Risk control
- Close (hedge) every position before the off unless you intend to hold;
  **leaving a trade open in-play by accident** is the classic big loss.
- Set a **maximum liability per market** and a daily stop-loss.
- Software ladders/one-click tools amplify mistakes — use test/practice
  modes first.
- Keep a log: entry, exit, ticks, P&L after commission.

## 6. Realism
- Exchanges are zero-sum between users minus commission; you profit only
  if your counterparties are worse. Many published "systems" don't survive
  commission.
- Some exchanges charge additional premium charges for consistently
  profitable accounts (check the terms).

## Responsible trading
Treat it as gambling: budget, time limits, self-exclusion tools. Losses can
come faster than in fixed-odds betting because of lay liabilities.

## Gotchas
- Confusing stake and liability on lays.
- Ignoring commission in green-up profit.
- Holding unmatched orders as the event starts.

## Verify
- [ ] Liability calculated and accepted before each lay.
- [ ] Can compute the equal-profit hedge for back-first and lay-first trades.
- [ ] Every pre-event position closed or deliberately held.
- [ ] P&L tracked net of commission.
