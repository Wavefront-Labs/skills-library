---
id: engineering-technology.technical-authentication-testing.reliability-testing.halt-and-accelerated-life-testing
name: halt-and-accelerated-life-testing
category: engineering-technology
field: technical-authentication-testing
product: reliability-testing
tags: [halt, hass, accelerated-life-testing, alt, step-stress, operating-limits, destruct-limits, proof-of-screen, arrhenius, activation-energy, acceleration-factor, coffin-manson, norris-landzberg, peck-model, thb, weibull-analysis, beta-shape-parameter, zero-failure-test, success-run, reliability-demonstration, thermal-cycling, random-vibration, environmental-testing, mtbf]
level: advanced
status: draft
description: "Run HALT step-stress to find operating/destruct limits, derive HASS with proof-of-screen, and plan ALT with Arrhenius/Coffin-Manson/Peck acceleration, Weibull fits and zero-failure sample sizes."
sources: ["Hobbs, G.K. Accelerated Reliability Engineering: HALT and HASS", "IEC 62506 Methods for product accelerated testing", "JEDEC JESD94 Application Specific Qualification Using Knowledge Based Test Methodology", "JEDEC JEP122 Failure Mechanisms and Models for Semiconductor Devices", "Abernethy, R.B. The New Weibull Handbook", "IEC 61649 Weibull analysis", "MIL-HDBK-781 Reliability Test Methods"]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# HALT and accelerated life testing — find the weak link, then quantify life

**Goal:** use HALT to expose design weaknesses fast, turn the margins into a production HASS screen, and use quantitative ALT to demonstrate a life or reliability target with stated confidence.

HALT is qualitative (find and fix); ALT is quantitative (predict and demonstrate). Do not quote a life number from HALT.

## 1. HALT step-stress (2-5 units, powered and monitored)

Run in a HALT chamber (LN2 cooling, repetitive-shock pneumatic 6-DOF table). Functionally monitor continuously; the definition of "fail" must be written down first.

1. **Cold step:** start at 20 °C, step −10 °C, dwell ~10 min after the product (not air) stabilises plus a functional test. Continue to the lower operating limit (LOL, recoverable fault) and destruct limit (LDL, permanent).
2. **Hot step:** same from 20 °C upward to UOL/UDL. Protect against fire; know your plastic and battery limits.
3. **Rapid thermal transitions:** cycle between ~LOL+5 °C and UOL−5 °C at the chamber's max rate (often 40-60 °C/min product air).
4. **Vibration step:** start ~5 Grms, step 5 Grms, dwell ~10 min; tap-test at each step (drop to ~5 Grms briefly) to find intermittents that only appear at low levels.
5. **Combined:** rapid thermal cycling with stepped vibration — usually the most productive stage.

At each failure: root-cause it (see engineering-technology.technical-authentication-testing.failure-analysis.fracture-surface-root-cause-analysis), fix or work around, continue. Stop pushing a stress when you reach a fundamental technology limit (e.g. solder melting, plastic Tg).

## 2. From HALT to HASS

- Typical starting screen: thermal extremes inside the operating limits (often ~80% of the way from ambient to the limit) and vibration around 50% of the destruct level — tune per product.
- **Proof of screen:** (a) seeded-defect units must be caught; (b) run the full screen 10-20 times on good units with no failures, showing the screen leaves ample life. Re-prove after design or process changes.
- Use HASA (audit sampling) once yields are stable.

## 3. Acceleration models (ALT)

Boltzmann k = 8.617×10⁻⁵ eV/K; temperatures in kelvin.

- **Arrhenius:** AF = exp[(Ea/k)·(1/T_use − 1/T_stress)]. Ea = 0.7 eV, 55 °C use, 125 °C stress: AF ≈ 78. Ea is mechanism-specific (roughly 0.3-1.1 eV); a wrong Ea changes AF by orders of magnitude, so justify it from JEP122 or your own data.
- **Coffin-Manson** (thermal-cycling fatigue): AF = (ΔT_stress/ΔT_use)^n, n ≈ 2 for solder joints (literature 1.9-2.7), 4+ for brittle cracking. −40/+125 °C test vs 40 °C field swing: (165/40)² ≈ 17. Norris-Landzberg adds dwell-time/frequency and T_max terms.
- **Peck** (temperature-humidity, e.g. 85 °C/85% RH THB): AF = (RH_s/RH_u)^n × Arrhenius term, commonly n ≈ 2.7, Ea ≈ 0.8 eV.
Stress levels must not introduce mechanisms absent in the field (stay below Tg, melting, or the HALT operating limit).

## 4. Weibull analysis

F(t) = 1 − exp[−(t/η)^β]. Plot with median ranks (Benard: (i − 0.3)/(n + 0.4)); use rank regression for n < ~20, MLE when many suspensions. β < 1 infant mortality (screen), β ≈ 1 random, β > 1 wear-out (design/maintenance). Fit each failure mode separately; mixing modes gives a meaningless dog-leg. Report B10 life with confidence bounds.

## 5. Zero-failure (success-run) sample size

Demonstrating reliability R at confidence C with no failures over one test life: n = ln(1 − C)/ln(R). R = 0.90, C = 90%: n = 22. With a known Weibull β and test duration L multiples of required life: n = ln(1 − C)/(L^β · ln R) — testing 2× life at β = 2 cuts n to ~6. For exponential MTBF tests: MTBF ≥ 2T/χ²(C; 2r + 2).

## Gotchas

- Measure product temperature with thermocouples on hot components; chamber air lies.
- HALT units are consumed — never ship them.
- Vibration energy in HALT tables is broadband and uncontrolled per axis; it does not replace qualification to a profile (e.g. MIL-STD-810, IEC 60068-2-64).
- A zero-failure test that sees one failure fails the demonstration; you cannot retest the same sample and pool.

## Verify

- [ ] Fail criteria and monitoring were defined before HALT.
- [ ] LOL/UOL/LDL/UDL and vibration limits are documented with root causes of each failure.
- [ ] HASS profile passed proof-of-screen (seeded defects caught, repeated screens without failure).
- [ ] Acceleration model and Ea/n values are justified and stay within one failure mechanism.
- [ ] Weibull fits are per failure mode with confidence bounds.
- [ ] Sample size and test duration meet the R/C target.
