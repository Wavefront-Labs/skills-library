---
id: engineering-technology.biomedical-engineering.device-verification-validation.equivalence-testing
name: equivalence-testing
category: engineering-technology
field: biomedical-engineering
product: device-verification-validation
tags: [tost, equivalence-testing, two-one-sided-tests, equivalence-margin, non-inferiority]
level: advanced
status: draft
description: "Demonstrate equivalence statistically with TOST: equivalence margin, hypotheses, confidence interval approach, sample size and common mistakes in device comparisons."
sources: ["Schuirmann, A comparison of the two one-sided tests procedure and the power approach (J Pharmacokinet Biopharm, 1987)", "FDA guidance on statistical methods for medical device comparisons (confirm current text)", "https://www.fda.gov"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Equivalence testing (TOST)

**Goal:** show two devices or processes differ by less than a defined, justified margin, rather than failing to find a difference.

## Why not a standard t-test
- A non-significant difference test only means lack of evidence of difference; with small samples or noisy data it proves nothing. Equivalence requires that the difference is demonstrably small.

## TOST procedure
1. **Define margin delta** (the largest difference that is not clinically or technically important) with justification before testing.
2. **Hypotheses:** null is that the true difference is outside the interval (at least delta in either direction); alternative is that it lies inside (-delta, +delta).
3. Perform two one-sided tests, each at significance level alpha (commonly 0.05); equivalence is concluded if both reject. This is equivalent to the **90 percent confidence interval** of the difference lying entirely within (-delta, +delta).
4. **Sample size:** for two groups with the same standard deviation sigma and a true difference of zero, n per group is about 2 times ((z at 1-alpha plus z at 1-beta/2) times sigma / delta) squared. Example: sigma = 1, delta = 0.5, alpha = 0.05 and power 80 percent give n of about 69 per group.
5. Analyse with a validated tool; check assumptions (normality, equal variance, paired versus independent designs); use the paired form for matched specimens.
6. Report the point estimate, confidence interval, margin and conclusion.

## Traps
- Choosing the margin after seeing the data.
- Using a 95 percent interval for a 0.05 TOST (conservative) or confusing the two.
- Applying to non-normal data without transformation or non-parametric methods.

## Verify
- [ ] Margin and its rationale fixed in the protocol.
- [ ] Sample size calculation documented.
- [ ] Interval-based conclusion reported.

> Practice guidance, not regulatory or clinical advice. Confirm current standard editions and rules for your jurisdiction, and defer to qualified regulatory, clinical and engineering judgement.
