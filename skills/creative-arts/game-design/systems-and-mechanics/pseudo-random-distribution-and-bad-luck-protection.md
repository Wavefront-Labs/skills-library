---
id: creative-arts.game-design.systems-and-mechanics.pseudo-random-distribution-and-bad-luck-protection
name: pseudo-random-distribution-and-bad-luck-protection
category: creative-arts
field: game-design
product: systems-and-mechanics
tags: [game-design, pseudo-random-distribution, bad-luck-protection, pity-timer, prd, randomness-design, probability-design, crit-chance, drop-rates, shuffle-bag]
level: advanced
status: draft
description: "Make random events feel fair: pseudo-random distribution (Dota-style PRD), pity timers, shuffle bags and streak breakers, with the maths to keep the average rate unchanged."
sources:
  - https://dota2.fandom.com/wiki/Random_Distribution
  - https://www.routledge.com/Game-Balance/Schreiber-Romero/p/book/9781498799577
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Pseudo-random distribution and bad-luck protection

**Goal:** keep the advertised average rate of a random event while cutting the long
streaks (of failure or success) that players perceive as unfair.

With true independent 25% chances, a player fails 8 times in a row with probability
0.75^8 = 10%. Over thousands of players, many see it every day and conclude the game is
broken.

## Techniques
### 1. Pseudo-random distribution (PRD)
Chance on the Nth attempt since the last success = `C x N`. C is chosen so the long-run
rate equals the nominal rate. Used in Dota 2 for crits and bashes; Dota's documented C
for a 25% nominal chance is about 0.0847 (first attempt 8.5%, rising each miss).
Compute C numerically:
```python
def prd_rate(c):  # long-run success rate for constant c
    p_none, exp_n, n = 1.0, 0.0, 0
    while p_none > 1e-12:
        n += 1; p = min(1.0, c * n)
        exp_n += n * p_none * p; p_none *= (1 - p)
    return 1 / exp_n
def find_c(target, lo=0.0, hi=1.0):
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if prd_rate(mid) < target else (lo, mid)
    return mid
assert abs(find_c(0.25) - 0.0847) < 0.001
```
### 2. Pity timer (bad-luck protection)
Guarantee a success after K consecutive failures (gacha "hard pity"), or increase the
chance after a threshold ("soft pity"). Recompute the effective average rate: a pity
cap *raises* it; publish the effective rate where law or platform requires odds
disclosure.
### 3. Shuffle bag
Put N outcomes in a bag (e.g. 1 success, 3 failures), draw without replacement, refill
when empty. Exact rate per bag; maximum streak is bounded (2N-2). Tetris's modern
"7-bag" randomiser is the famous example.
### 4. Streak breakers
Simple rule: after X failures, force success (or after Y successes, force a failure on
enemy-favourable rolls).

## Choosing
| Need | Use |
|---|---|
| combat procs, crits | PRD |
| rare loot / gacha | pity timer + disclosed effective odds |
| level/piece generation | shuffle bag |
| quick fix in tabletop | deck of cards instead of dice |

## Gotchas
- PRD makes the next proc partially predictable; competitive players will track it.
- Pity counters must persist correctly (per banner, per account) and be documented.
- Changing a rate after launch without updating disclosed odds may breach platform
  rules (e.g. Apple's guideline requiring loot-box odds disclosure).

## Verify
- [ ] Simulated 1e6 trials: long-run rate equals the nominal (or disclosed) rate.
- [ ] Max failure streak measured and acceptable.
- [ ] Rate disclosure updated where required.
