---
id: mind-self.decision-making-and-problem-solving.decision-trees-and-expected-value.choosing-under-uncertainty-with-expected-value
name: choosing-under-uncertainty-with-expected-value
category: mind-self
field: decision-making-and-problem-solving
product: decision-trees-and-expected-value
tags: [decision-making-and-problem-solving, decision-tree, expected-value, ev, probability, payoff, risk, uncertainty, risk-of-ruin, risk-tolerance, utility, value-of-information, rollback, base-rates, calibration, scenario-analysis, decision-analysis, insurance-decisions, bayesian-thinking]
level: practitioner
status: draft
description: "Lay out a choice as a decision tree with probabilities and payoffs, roll back expected values, then check risk of ruin, risk tolerance and whether more information is worth buying."
sources: ["Raiffa, Decision Analysis (1968)", "Clemen & Reilly, Making Hard Decisions, 3rd ed. (2013)", "Hammond, Keeney & Raiffa, Smart Choices (1999)", "Tetlock & Gardner, Superforecasting (2015)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Choosing under uncertainty with expected value

**Goal:** make a better choice when outcomes depend on chance — launch or wait, settle or
go to court, buy the extended warranty, take the risky job — by mapping outcomes,
estimating probabilities and comparing on both average result and worst case.

## 1. Draw the tree
- **Square** = a decision you control. **Circle** = a chance event. **Triangle / end** =
  an outcome with a payoff.
- Start at the left with the decision; draw a branch for each option.
- On each option, add the chance events that follow, with their possible outcomes.
- Keep it small: 2–4 options, 2–3 outcomes per chance node. Big trees hide guesses.

## 2. Put numbers on it
- **Payoffs** at each end: money, time, or a 0–100 score. Include all costs (fees, time,
  stress if you can value it).
- **Probabilities** on each chance branch, summing to 1 at each circle. Sources, in order
  of preference: data/base rates ("what fraction of similar cases…"), expert estimates,
  your own calibrated guess.
- When guessing, give ranges, and anchor on the **base rate** for similar situations
  before adjusting for specifics (Tetlock's outside-view advice).

## 3. Roll back
From the right: at each chance node, **EV = Σ (probability × payoff)**. At each decision
node, pick the branch with the best EV (for now). Work back to the root.

### Worked example: settle or go to court
- Settle: receive £20,000 for certain → EV £20,000.
- Court: 60% win £45,000; 40% lose and get £0; legal costs £8,000 either way.
  EV = 0.6 × 45,000 + 0.4 × 0 − 8,000 = **£19,000**.
EV is close, but court has a 40% chance of a −£8,000 result. Most people should settle —
which leads to step 4. (Figures illustrative.)

## 4. Check risk, not just averages
- **Risk of ruin:** if any branch leads to an outcome you can't survive or recover from
  (bankruptcy, losing your home, serious injury), the EV maths doesn't apply — avoid it
  or insure against it.
- **Risk tolerance:** how much of the spread can you live with? Replace money with a
  utility score that reflects that a loss hurts more than an equal gain helps.
- **Repeated vs one-off:** EV is the right guide for decisions you make many times
  (pricing, small bets); for one-off big decisions, weight the downside more.

## 5. Value of information
Before deciding, ask: what would change the choice? If one probability (say, the chance
of winning in court) would flip the decision when moved within its plausible range,
then information that narrows it (a second legal opinion, a pilot test, a survey) may be
worth paying for. Rough rule: it's worth at most the EV improvement from deciding with it.

## 6. Sensitivity
Vary each probability and payoff across its plausible range; find the **break-even
point** where the preferred option changes. If your estimate is far from break-even,
decide. If close, gather information or pick the more reversible option.

## Gotchas
- **Garbage in:** precise outputs from guessed probabilities look authoritative — always
  show the ranges.
- **Missing branches:** the "something else happens" outcome is usually under-weighted.
- **Overconfidence:** people's 90% ranges contain the truth far less than 90% of the time;
  widen them.
- **Sunk costs** belong nowhere in the tree; only future costs and payoffs count.
- Not legal or financial advice; for big stakes, check numbers with a professional.

## Verify
- [ ] Probabilities at each chance node sum to 1 and have a stated source or range.
- [ ] Every payoff includes all costs, and sunk costs are excluded.
- [ ] You rolled back EVs correctly (spot-check one by hand).
- [ ] You checked the worst-case branch for ruin.
- [ ] You know the break-even point for the most uncertain number.
