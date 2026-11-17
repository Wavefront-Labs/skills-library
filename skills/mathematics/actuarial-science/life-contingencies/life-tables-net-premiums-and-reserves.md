---
id: mathematics.actuarial-science.life-contingencies.life-tables-net-premiums-and-reserves
name: life-tables-net-premiums-and-reserves
category: mathematics
field: actuarial-science
product: life-contingencies
tags: [life-contingencies, actuarial-science, life-table, mortality-table, lx, dx, qx, px, survival-probability, annuity, annuity-due, whole-life-assurance, term-assurance, endowment, net-premium, equivalence-principle, policy-reserve, prospective-reserve, thiele, commutation-functions, actuarial-present-value, soa-ltam, ifoa-cm1, udd]
level: practitioner
status: verified
description: "From a life table to actuarial present values, net premiums via the equivalence principle, and prospective policy reserves, with the timing and fractional-age traps."
sources: ["Dickson, Hardy & Waters, Actuarial Mathematics for Life Contingent Risks (CUP)", "Bowers et al., Actuarial Mathematics (SOA)"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Life tables, net premiums and reserves

**Goal:** value a life-contingent payment stream correctly — price it with the
equivalence principle, then hold the right reserve at each duration — and know
where the hand calculations go wrong.

## 1. Read the life table
A life table gives `l_x` (survivors at exact age x from a radix like 100,000).
- `d_x = l_x − l_{x+1}`, `q_x = d_x / l_x`, `p_x = 1 − q_x`.
- `t_p_x = l_{x+t} / l_x` (survive t years), `t|q_x = (l_{x+t} − l_{x+t+1}) / l_x`
  (die in year t+1).
- Check: `Σ d_x` over all ages equals the radix; `q_ω−1 = 1` at the last age.

**Gotcha — select vs ultimate.** A select table (e.g. `q_[x]+t`) gives lower
mortality for recently underwritten lives. Using the ultimate column for a newly
issued policy overstates mortality and misprices term business.

## 2. Actuarial present values (APVs)
With `v = 1/(1+i)`:
- Whole-life assurance, benefit end of year of death: `A_x = Σ_k v^{k+1} k_p_x q_{x+k}`.
- Term-n assurance: same sum, k = 0 … n−1.
- Pure endowment: `n_E_x = v^n n_p_x`.
- Whole-life annuity-due: `ä_x = Σ_k v^k k_p_x`.
- Key identity: `A_x = 1 − d·ä_x` with `d = i/(1+i)`. Use it as a check, not a shortcut
  you cannot verify.
- Recursion is the easiest spreadsheet route: `A_x = v(q_x + p_x A_{x+1})`, start at
  the last age with `q = 1` (where `A = v` and `ä = 1`), work down. Same for `ä_x = 1 + v p_x ä_{x+1}`.

Commutation functions (`D_x = v^x l_x`, `N_x`, `C_x`, `M_x`) still appear in exams and
old systems: `ä_x = N_x/D_x`, `A_x = M_x/D_x`. They are equivalent, just pre-computed.

## 3. Net premium by the equivalence principle
Set APV(premiums) = APV(benefits). For whole life, benefit S, annual premiums in advance:
`P = S · A_x / ä_x`. For limited-pay or endowment, change the sums' ranges, not the method.
Gross premiums add expenses to the benefit side (initial + renewal + claim expenses)
with premium-related expenses as a fraction of P.

## 4. Reserves
Prospective net premium reserve at duration t (just before premium t):
`tV = S·A_{x+t} − P·ä_{x+t}`.
- `0V = 0` at issue under the equivalence principle — a quick check.
- Recursive (Thiele's discrete form): `(tV + P)(1+i) = q_{x+t}·S + p_{x+t}·(t+1)V`.
  Building reserves forward with this recursion and comparing to the prospective
  formula catches most spreadsheet errors.
- For an endowment the reserve climbs to S at maturity; for term assurance it rises
  then falls to 0. A negative reserve usually means a premium pattern mismatch.

## 5. Fractional ages and timing
Real policies pay monthly and claims occur mid-year.
- **UDD** (uniform distribution of deaths): `A_x^(continuous) ≈ (i/δ) A_x`;
  `ä_x^(m) ≈ α(m) ä_x − β(m)` (with α ≈ 1, β ≈ (m−1)/2m for small i).
- The crude "subtract (m−1)/2m" approximation is fine for checks, not for pricing.
- Be explicit about **in advance vs in arrears** and **end of year vs moment of death**:
  most wrong answers are timing, not maths.

## Uncertainty notes
The formulas are standard (SOA LTAM syllabus, whose core text is Dickson, Hardy and Waters, confirmed on soa.org; all identities here were recomputed in Python on a Makeham table at i = 5%: sum of d = radix, A + d·ä = 1 to 1e-15, direct sum = recursion = N/D and M/D forms, 0V = 0, Thiele recursion matches prospective reserve to 3e-8, exact UDD monthly annuity = α·ä − β to 1e-12; at i = 5% and m = 12, α = 1.0002 and β = 0.4665 against the small-i approximation 0.4583). Exact UDD α(m), β(m) values
depend on i; compute them rather than quoting from memory. Statutory reserving bases
(e.g. regulator-prescribed valuation interest and tables) vary by jurisdiction and are
out of scope.

## Verify
- [ ] `Σ d_x` = radix and every `q_x` ∈ [0,1].
- [ ] `A_x + d·ä_x = 1` holds to rounding at several ages.
- [ ] `0V = 0`, and the retrospective/recursive reserve matches the prospective one.
- [ ] Endowment reserve reaches S at maturity; term reserve returns to 0.
- [ ] Select vs ultimate, in advance vs arrears and fractional-age assumption are stated.
