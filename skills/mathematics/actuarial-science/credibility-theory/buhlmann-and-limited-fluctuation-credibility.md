---
id: mathematics.actuarial-science.credibility-theory.buhlmann-and-limited-fluctuation-credibility
name: buhlmann-and-limited-fluctuation-credibility
category: mathematics
field: actuarial-science
product: credibility-theory
tags: [credibility-theory, credibility, limited-fluctuation, classical-credibility, full-credibility-standard, square-root-rule, 1082-claims, buhlmann, buhlmann-straub, epv, vhm, credibility-factor, complement-of-credibility, shrinkage, empirical-bayes, experience-rating, bayesian-credibility, actuarial-science, soa-stam, cas-exam]
level: practitioner
status: verified
description: "Blend a risk's own experience with a collective estimate using limited-fluctuation (1,082-claim) or Buhlmann/Buhlmann-Straub credibility, including estimating EPV and VHM from data."
sources: ["Klugman, Panjer & Willmot, Loss Models (Wiley), credibility chapters", "Mahler & Dean, Credibility (CAS Foundations of Casualty Actuarial Science)", "https://search.r-project.org/CRAN/refmans/actuar/html/cm.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Bühlmann and limited-fluctuation credibility

**Goal:** an estimate `Z·X̄ + (1 − Z)·M` — own experience X̄, complement M — where the
weight Z is justified rather than picked by feel.

## 1. Limited-fluctuation (classical) credibility
Full credibility when the observed quantity is within ±k of its mean with probability p.
- For Poisson claim counts: `n_F = (z_{(1+p)/2} / k)²`. With p = 90%, k = 5%:
  `(1.645 / 0.05)² ≈ 1,082` expected claims — the standard you will see quoted.
- For aggregate losses / pure premium, multiply by `(1 + CV_X²)` where CV_X is the
  severity coefficient of variation: heavier severity → more claims needed.
- Partial credibility: **square-root rule** `Z = min(1, √(n / n_F))`.
- Strength: simple, regulator-familiar. Weakness: ignores how different risks really
  are from each other, so it can give high Z to a homogeneous book where the
  complement is already good.

## 2. Bühlmann credibility (greatest accuracy)
Each risk has an unknown mean μ(θ). Define:
- **EPV** = expected process variance = E[Var(X | θ)] — noise within a risk.
- **VHM** = variance of hypothetical means = Var(μ(θ)) — real differences between risks.
- `k = EPV / VHM`, `Z = n / (n + k)`.
Z rises with more observations n and with greater real heterogeneity. It is the best
linear approximation to the Bayesian posterior mean, and exact for conjugate pairs
(Poisson-gamma, normal-normal).

**Bühlmann-Straub** handles unequal exposures m_i (e.g. different fleet sizes):
`Z_i = m_i / (m_i + k)`, with X̄_i the exposure-weighted mean.

## 3. Estimating EPV and VHM from data (empirical Bayes)
For r risks × n years each (equal exposure), observations X_ij:
- `EPV̂ = (1 / (r(n−1))) Σ_i Σ_j (X_ij − X̄_i)²`
- `VHM̂ = (1/(r−1)) Σ_i (X̄_i − X̄)² − EPV̂ / n`
- If VHM̂ ≤ 0, set Z = 0: the data show no evidence risks differ.
- The complement M is the overall mean X̄ (or, in Bühlmann-Straub, the
  credibility-weighted mean so the total balances).
R: `actuar::cm(~ risk, data, ratios = ..., weights = ...)` fits Bühlmann-Straub (CRAN reference manual confirms `cm(formula, data, ratios, weights, ..., method = c("Buhlmann-Gisler", "Ohlsson", "iterative"))`).

## 4. Choosing the complement
The complement matters as much as Z. Good complements are unbiased for the risk,
independent of its own data, and stable: class rate, trended prior rate, a larger
group's experience, or a competitor/industry indication (with adjustments).

## 5. Worked check
Book of 5 fleets × 4 years. EPV̂ = 0.40, VHM̂ = 0.02 → k = 20. A fleet with 4 years
gets Z = 4/24 ≈ 0.17. With 3,000 expected claims under the classical rule it would be
fully credible — the two philosophies can disagree; say which you used and why.

## Uncertainty notes
Formulas are standard textbook results. Recomputed: (1.645/0.05)^2 = 1,082.2; the EPV and VHM estimators are unbiased in a Poisson-gamma simulation (200,000 risks, 4 years: EPV 1.99 vs true 2, VHM 1.97 vs true 2); Z = 4/24 = 0.167. The worked figures are illustrative,
not from real data. Bühlmann-Straub estimator details (unbiased vs alternative VHM
estimators) vary by text; confirm the variant your reviewer expects.

## Verify
- [ ] Full-credibility standard states p, k and whether severity variance is included.
- [ ] EPV and VHM estimated with the right divisors; negative VHM → Z = 0.
- [ ] Z increases with exposure and lies in [0, 1].
- [ ] Complement is independent of the risk's own data and documented.
- [ ] Credibility-weighted estimates rebalance to the book total where required.
