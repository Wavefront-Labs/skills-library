---
id: sports-recreation.gambling-and-wagering.bankroll-management.staking-plans-kelly-and-loss-limits
name: staking-plans-kelly-and-loss-limits
category: sports-recreation
field: gambling-and-wagering
product: bankroll-management
tags: [gambling-and-wagering, bankroll-management, bankroll, staking, staking-plan, flat-staking, units, kelly-criterion, kelly, fractional-kelly, half-kelly, variance, drawdown, risk-of-ruin, expected-value, martingale, chasing-losses, stop-loss, loss-limit, deposit-limit, session-limit, self-exclusion, poker-bankroll, buy-ins, responsible-gambling, tilt]
level: practitioner
status: draft
description: "Bankroll management for any wagering: separate bankroll, flat staking vs Kelly and fractional Kelly, variance and drawdowns, and hard loss and time limits."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Bankroll management — staking, Kelly and loss limits

**Goal:** size bets so that normal bad runs don't wipe you out, and set
limits that keep gambling affordable. Bankroll management cannot turn a
negative-EV game into a winner; it only controls *how fast* money moves
and protects against ruin if you do have an edge.

## 1. Separate the bankroll
- A **bankroll** is money set aside only for wagering, that you can lose
  entirely without affecting bills, savings or debt repayments.
- Never top it up from essential money. Never borrow to gamble.
- Track it separately (its own account/e-wallet or a spreadsheet).

## 2. Units and flat staking
- Define **1 unit** as a fixed % of bankroll — commonly **1–2%** for sports
  bettors. With a £1,000 bankroll, 1 unit = £10–£20.
- **Flat staking:** same unit on every bet (or 1–3 units by confidence).
  Simple, robust, and the right default for most people.
- Recalculate unit size at set intervals (e.g. monthly), not after every bet.

## 3. Kelly criterion
For a bet with decimal odds *d* (b = d − 1 net odds) and your estimated win
probability *p* (q = 1 − p):
`Kelly fraction f* = (b·p − q) / b`
- Example: odds 2.50 (b = 1.5), p = 0.45 → f* = (0.675 − 0.55) / 1.5 =
  **8.3%** of bankroll.
- If f* ≤ 0, there's no edge — **don't bet**.
- Full Kelly maximises long-run growth *only if p is accurate*. Since
  estimates are always overconfident, most practitioners use **fractional
  Kelly** (¼ to ½), which cuts volatility sharply for a modest growth cost.
- Kelly with a wrong p over-bets and can be ruinous. If you can't
  demonstrate an edge (e.g. via closing line value), use flat staking.

## 4. Variance and drawdowns
- Even a genuine 3% edge at around even odds produces long losing streaks;
  drawdowns of 20–30+ units over a few hundred bets are normal.
- **Sample size:** hundreds to thousands of bets are needed before results
  separate skill from luck.
- **Poker** convention (rough guidance): cash games ~20–40+ buy-ins at
  the stake played, tournaments much more (often 100+ buy-ins) due to
  higher variance. **Community rules of thumb, not proven thresholds.**

## 5. Systems that don't work
- **Martingale** (double after each loss): small frequent wins, then a
  catastrophic loss when a streak hits table limits or bankroll. It does
  not change expected value.
- "Due" outcomes, progressive staking after losses, and chasing — all
  increase risk without edge.

## 6. Limits (the most important part)
Set before you start, write them down, and use the operator's tools:
- **Deposit limit** (daily/weekly/monthly) in each account.
- **Loss limit** per session and per month; stop for the day when hit.
- **Time limit** / reality checks.
- **Cooling-off** and **self-exclusion** (operator-level, and national
  schemes such as GAMSTOP in the UK or state self-exclusion registers —
  check local options), plus bank gambling blocks offered by many banks.
- Warning signs: chasing losses, hiding gambling, borrowing, gambling to
  escape stress. Contact local gambling support services early.

## 7. Record keeping
Log stake, odds, result and bankroll balance. Review ROI and maximum
drawdown monthly. Tilted periods show up clearly in a log.

## Gotchas
- Raising stakes after wins ("house money") or losses (chasing).
- Using full Kelly with guessed probabilities.
- Multiple accounts with no combined view.

## Verify
- [ ] Bankroll defined, separate, and affordable to lose.
- [ ] Unit size written and fixed for the period.
- [ ] Kelly used only with a demonstrated edge, and fractionally.
- [ ] Deposit, loss and time limits set in every account.
