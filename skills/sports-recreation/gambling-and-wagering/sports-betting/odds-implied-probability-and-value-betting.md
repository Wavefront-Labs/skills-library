---
id: sports-recreation.gambling-and-wagering.sports-betting.odds-implied-probability-and-value-betting
name: odds-implied-probability-and-value-betting
category: sports-recreation
field: gambling-and-wagering
product: sports-betting
tags: [gambling-and-wagering, sports-betting, betting, wagering, odds, decimal-odds, fractional-odds, american-odds, moneyline, implied-probability, overround, vig, vigorish, juice, margin, value-betting, expected-value, ev, line-shopping, closing-line-value, clv, handicap, spread, totals, over-under, accumulator, parlay, form-study, horse-racing, responsible-gambling]
level: practitioner
status: draft
description: "Sports betting fundamentals: converting decimal, fractional and American odds to implied probability, removing the bookmaker margin, spotting value, line shopping and record keeping."
sources: []
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Sports betting — odds, implied probability and value

**Goal:** understand what a price means, how much the bookmaker keeps, and
when a bet has positive expected value. Most bettors lose over time
because of the built-in margin; this skill shows the arithmetic so
decisions are made with eyes open. **Gamble only what you can afford to
lose; see bankroll-management and use deposit limits.**

## 1. Odds formats and implied probability
| Format | Example | Implied probability |
|---|---|---|
| Decimal | 2.50 | 1 / 2.50 = **40%** |
| Fractional | 3/2 | 2 / (3+2) = **40%** |
| American + | +150 | 100 / (150+100) = **40%** |
| American − | −200 | 200 / (200+100) = **66.7%** |
Decimal odds include your stake: a $10 bet at 2.50 returns $25 ($15 profit).

## 2. The margin (overround / vig)
Add the implied probabilities of all outcomes in a market:
- Two-way market at 1.91 / 1.91 → 52.4% + 52.4% = **104.8%**. The 4.8% over
  100 is the bookmaker's overround (≈4.5% margin on turnover).
- To estimate "fair" probabilities, divide each implied probability by the
  total (simple proportional method): 52.4 / 104.8 = 50%. Other methods
  (e.g. power, Shin) adjust for favourite-longshot bias.
- Accumulators/parlays **multiply margins** across legs — that's why they're
  heavily promoted.

## 3. Expected value
`EV per unit stake = (your probability × decimal odds) − 1`
- You think a team wins 45%; price is 2.40 → 0.45 × 2.40 − 1 = **+0.08**
  (+8%). At 2.10 → −5.5%.
- "Value" exists only if your probability is more accurate than the
  market's. Most of the time the market (especially at closing in liquid
  markets) is very efficient.

## 4. Line shopping
- Prices differ between bookmakers. Taking 2.10 instead of 2.00 on every
  bet is a 5% better return for free. Keep accounts with several licensed
  operators (where legal) and compare, or use odds-comparison sites.
- **Closing line value (CLV):** if you consistently get better prices than
  the final (closing) price, that's the best evidence you have an edge.
  Results alone over small samples are mostly noise.

## 5. Common markets
- **Moneyline / 1X2** (win/draw/win), **handicap/spread** (team gives or
  receives points), **totals** (over/under), props, futures.
- Asian handicap with quarter lines splits stake across two lines.
- **Racing:** form study (recent runs, class, distance, going/track
  condition, weight, draw, jockey/trainer form); each-way bets pay a
  fraction of win odds for a place — check the place terms.

## 6. Record keeping
Log every bet: date, market, odds taken, closing odds, stake, result,
reasoning. Calculate ROI = profit / total staked, and CLV average. Review
monthly. Many bettors who "feel" they're winning find they're not.

## 7. Practical notes
- Successful bettors may face **stake restrictions** from bookmakers.
- Bonuses carry wagering requirements; read terms.
- Betting is regulated and age-limited; legality varies by country/state.
- Never bet on events you're involved in (integrity rules).

## Responsible gambling
Set deposit and time limits in your account, use self-exclusion tools
if needed (e.g. national schemes such as GAMSTOP in the UK — check local
equivalents), and don't chase losses. Seek help from local gambling
support services if betting stops being fun.

## Gotchas
- Confusing American −/+ conversions.
- Thinking a winning month means skill.
- Multi-leg parlays for "value".

## Verify
- [ ] Can convert any odds format to implied probability.
- [ ] Can compute the overround of a market.
- [ ] Every bet logged with odds taken and closing odds.
- [ ] Deposit limit set on each account.
