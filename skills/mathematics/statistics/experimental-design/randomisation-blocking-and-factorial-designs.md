---
id: mathematics.statistics.experimental-design.randomisation-blocking-and-factorial-designs
name: randomisation-blocking-and-factorial-designs
category: mathematics
field: statistics
product: experimental-design
tags: [statistics, experimental-design, design-of-experiments, doe, randomisation, randomization, blocking, randomised-block-design, factorial-design, fractional-factorial, interaction, replication, sample-size, power, a-b-testing, ab-test, cluster-randomisation, crossover-design, anova, pseudoreplication, cuped, sample-ratio-mismatch]
level: practitioner
status: verified
description: "Design experiments that answer the question: randomise properly, block on known nuisance factors, use factorials instead of one-factor-at-a-time, and size the study."
sources:
  - https://pypi.org/project/pyDOE3/
  - https://cran.r-project.org/package=FrF2
  - https://www.statsmodels.org/stable/generated/statsmodels.stats.power.NormalIndPower.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Randomisation, blocking and factorial designs

**Goal:** design a study where the comparison you care about is unbiased, precise
enough to matter, and analysable with a model you chose in advance.

## 1. Fix the three units
- **Experimental unit** — the thing that is independently assigned a treatment (a
  plot, a patient, a classroom, a user). Its count is your real n.
- **Observational unit** — what you measure (leaf, visit, page view).
- **Treatment factors and levels.**
Measuring 30 plants in each of 2 greenhouses, one per treatment, is n = 1 per arm,
not 30 — **pseudoreplication**. When whole groups are assigned, analyse at group level
or with a mixed model, and size the study with the design effect (see
mathematics.statistics.survey-sampling.survey-weighting-and-design-effects).

## 2. Randomise — with a recorded seed
Randomisation balances unknown confounders on average and justifies the analysis.
- Generate the allocation in code with a fixed seed and keep the list
  (`set.seed(2026); sample(rep(c("A","B"), each = 20))`).
- **Conceal** the allocation from whoever enrols units; predictable alternation
  (A, B, A, B) lets people steer units.
- Use **permuted blocks** (block size varying, e.g. 4 and 6) to keep arms balanced
  over time without being guessable.

## 3. Block on what you know
If a nuisance factor strongly affects the outcome (day, batch, machine, site, litter),
**block** on it: randomise treatments *within* each block, and include block in the
model (`y ~ treatment + block`). Rule: "block what you can, randomise what you can't."
Blocking that doesn't correlate with the outcome costs only a few error df.
Paired and crossover designs are the extreme case — each unit is its own block
(crossovers need a washout and assume no carry-over).

## 4. Use factorials, not one-factor-at-a-time
To study temperature (2 levels) and time (2 levels), run all 4 combinations (a 2²
factorial) rather than varying one at a time. Benefits:
- Every run informs both main effects — same precision for fewer runs.
- You can estimate the **interaction** (does the effect of time depend on temperature?);
  OFAT cannot.
For k factors, 2^k runs grows fast; a **fractional factorial** (2^(k−p)) estimates main
effects with fewer runs at the price of **aliasing** some interactions. Resolution IV or
higher keeps main effects clear of two-factor interactions. Add centre points to detect
curvature. Tools: R `FrF2`, Python `pyDOE3` (`fracfact`, `ff2n`; the older `pyDOE2` 1.3.0 fails on import under Python 3.12+ because it imports the removed `imp` module), Minitab/JMP DOE menus. Checked: the 2^(4-1) design `fracfact('a b c abc')` is Resolution IV, main effects uncorrelated with every two-factor interaction, but ab is fully aliased with cd.

## 5. Size it
Sample size per arm for comparing means: n ≈ 15.7·(σ/δ)² at alpha 0.05, 80% power
(details in mathematics.statistics.statistical-inference.hypothesis-test-and-confidence-interval-workflow).
For two proportions p1, p2: n ≈ 7.85·[p1(1−p1) + p2(1−p2)] / (p1 − p2)².
Example: 10% → 12% conversion needs ≈ 7.85 × (0.09 + 0.1056) / 0.0004 ≈ 3,840 per arm (statsmodels `NormalIndPower` with Cohen's h gives about 3,835).
Blocking or a baseline covariate (ANCOVA; CUPED in A/B testing) can shrink the needed
n substantially when the covariate is strongly correlated with the outcome.

## 6. Online A/B tests: extra checks
- **Sample ratio mismatch:** if a 50/50 split arrives as 50.8/49.2, run a
  chi-squared goodness-of-fit test (p = 0.61 at n = 1,000, 0.11 at 10,000, 4e-7 at 100,000; so it matters only at large n); a tiny p means assignment or logging is broken — don't read the result.
- Fix the duration in whole weeks to cover weekday effects; don't stop on first significance.
- Randomise by user, not page view, unless the metric is per view.

## 7. Pre-register the analysis
Write the primary outcome, model, covariates and sample size before data arrive.
Secondary outcomes are exploratory.

## Gotchas
- Confusing experimental and observational units — the commonest design error.
- Running all of treatment A on Monday and B on Tuesday confounds treatment with day.
- Dropouts that differ by arm break randomisation; analyse by intention to treat.
- Uncertain: the proportions formula above is the normal approximation; for small
  rates or unequal arms use a dedicated calculator (`power.prop.test`, G*Power).

## Verify
- [ ] Experimental unit identified; n counts those units.
- [ ] Allocation generated by code with a saved seed and concealed.
- [ ] Known nuisance factors blocked and included in the model.
- [ ] Factors crossed (factorial/fractional) rather than varied one at a time.
- [ ] Sample size computed from a stated minimal effect and variance.
- [ ] Analysis plan written down before results.
