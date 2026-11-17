---
id: mind-self.critical-thinking-and-argumentation.calibration-and-probabilistic-reasoning.calibration-training-and-bayesian-updating
name: calibration-training-and-bayesian-updating
category: mind-self
field: critical-thinking-and-argumentation
product: calibration-and-probabilistic-reasoning
tags: [calibration-and-probabilistic-reasoning, calibration, credence, probability, bayesian-updating, bayes-theorem, likelihood-ratio, odds, brier-score, forecasting, superforecasting, prediction-log, confidence-intervals, overconfidence, metaculus, good-judgment, base-rate, critical-thinking, rationality]
level: practitioner
status: draft
description: "Put numbers on beliefs, update them with likelihood ratios in odds form, keep a prediction log, and score yourself with Brier scores and calibration buckets."
sources: ["Tetlock & Gardner, Superforecasting (2015)"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Calibration training and Bayesian updating

**Goal:** hold beliefs as probabilities, change them by the right amount when evidence
arrives, and check over time that your "70%" things happen about 70% of the time.

## 1. Assign a credence
For any belief that matters, write a number: "I'm 80% sure the contractor finishes by
June." Rules of thumb:
- Avoid 0% and 100% for anything empirical — no evidence could then move you.
- Use the full range; "50%" for everything uncertain is a way of not committing.
- Make the claim **resolvable**: a clear outcome and a date ("by 30 June, per the sign-off").

## 2. Start from a base rate
Begin with how often things like this happen (the outside view; see
cognitive-bias-mitigation), then adjust for specifics.

## 3. Update with odds and likelihood ratios
Bayes' rule is easiest in **odds form**:
`posterior odds = prior odds × likelihood ratio`
- Convert probability to odds: 20% → 1:4. Odds to probability: 1:4 → 1/(1+4) = 20%.
- **Likelihood ratio (LR)** = how much more likely you'd see this evidence if the claim
  were true than if it were false.
- Worked example: prior 20% (1:4) that a supplier is unreliable. They miss a deadline.
  Suppose unreliable suppliers miss ~60% of deadlines and reliable ones ~15%: LR = 4.
  Posterior odds = 1:4 × 4 = 1:1 → **50%**. Not "now I'm sure", not "ignore it".
- Evidence with LR near 1 (equally likely either way) should barely move you, however
  vivid it is.

## 4. Keep a prediction log
A spreadsheet with columns: date, claim, probability, resolution date, outcome (1/0),
notes on reasoning. Ten to twenty predictions a month is enough to learn from within
a year. Public forecasting platforms (e.g. Metaculus, Good Judgment Open) give
ready-made questions and scoring; check their current terms yourself.

## 5. Score yourself
- **Brier score** for yes/no questions: average of `(forecast − outcome)²`, where outcome
  is 1 or 0. 0 is perfect; always saying 50% scores 0.25. Lower is better.
- **Calibration table:** group predictions into buckets (50–59%, 60–69%, … 90–99%) and
  compare the bucket's average forecast to the fraction that came true. Overconfident
  people see their 90% bucket coming true far less than 90%.
- With few predictions per bucket the table is noisy; read it after 50+ resolved items.

## 6. Calibrate ranges too
For estimates ("how long will this take?") give a 90% interval: low and high bounds you
are 90% sure contain the truth. Most people's "90%" intervals contain the answer only
about half the time — widen them until your hit rate approaches 9 in 10.

## Gotchas
- **Resolution creep:** vague claims get judged generously afterwards. Fix criteria first.
- **Updating on the same evidence twice** (hearing one report from three outlets).
- **Big swings from one anecdote** — check the LR, not the vividness.
- **Calibration ≠ accuracy:** someone who says 60% to everything with a 60% hit rate is
  calibrated but uninformative. Aim for confident *and* calibrated.
- Likelihood figures in the worked example are illustrative, not real supplier data.

## Verify
- [ ] Each belief tracked has a number, a resolution criterion and a date.
- [ ] Updates are explained as prior × LR, not as gut jumps.
- [ ] A prediction log exists and is reviewed at least monthly.
- [ ] You know your Brier score and how your 70–90% buckets actually performed.
- [ ] Your 90% intervals contain the truth roughly 9 times in 10.
