---
id: health-medicine.pharmacy.pharmacokinetic-dosing.vancomycin-auc-guided-dosing-and-tdm
name: vancomycin-auc-guided-dosing-and-tdm
category: health-medicine
field: pharmacy
product: pharmacokinetic-dosing
tags: [pharmacokinetic-dosing, pharmacy, clinical-pharmacokinetics, vancomycin, tdm, therapeutic-drug-monitoring, auc, auc-mic, auc24, trough, peak, two-level-kinetics, bayesian-dosing, first-order-kinetics, elimination-rate-constant, half-life, loading-dose, renal-dosing, aki, nephrotoxicity, mrsa, ashp-idsa-2020, crcl, cockcroft-gault, obesity-dosing, pediatric-vancomycin]
level: advanced
status: gated
description: "Dose vancomycin to an AUC24 of 400-600: loading dose, Bayesian vs two-level first-order calculation, sampling timing, worked adjustment, AKI handling and common TDM errors."
sources: ["https://pmc.ncbi.nlm.nih.gov/articles/PMC7358040", "https://pubmed.ncbi.nlm.nih.gov/32227354/"]
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Vancomycin AUC-guided dosing and TDM

> General professional reference. Loading-dose limits, AUC target and monitoring recommendations were checked against the 2020 ASHP/IDSA/PIDS/SIDP guideline text (PMC7358040); other figures are marked. Confirm against the current guideline and your institution's protocol/nomogram before use. Pediatric and neonatal regimens differ and are institution-specific.

**Goal:** reach an effective exposure for serious MRSA infection (AUC24/MIC 400–600,
assuming MIC 1 mg/L) quickly, while avoiding the nephrotoxicity that rises with AUC >600
and with trough-chasing to 15–20 mg/L.

## 1. Start: loading dose + empiric maintenance
- **Loading dose** (serious infection, critically ill, dialysis): 20–35 mg/kg **actual body
  weight**, maximum 3,000 mg (2020 guideline Rec 12; 20–25 mg/kg in obesity, Rec 13). The
  guideline gives no infusion rate; product labelling is said to limit infusion to no faster than 10 mg/min and at
  least 60 min per dose, whichever is longer (gated: unconfirmed, source is paywalled or blocked), so large loading doses run over several hours, to limit
  infusion reactions ("vancomycin flushing"). Confirm against the current label.
- **Maintenance:** from a population model / Bayesian software or nomogram, typically
  15–20 mg/kg every 8–12 h with normal renal function (gated: unconfirmed, source is paywalled or blocked). Estimate CrCl (Cockcroft–Gault)
  but treat the estimate as unreliable in unstable renal function, very low muscle mass,
  amputees, and extremes of weight.

## 2. Monitoring method: Bayesian preferred, two-level acceptable
- **Bayesian software** can use one level (even a trough) plus a population prior, and
  can be used before steady state — preferred by the consensus.
- **Two-level first-order method** (when no software): draw a post-distribution **peak**
  (the guideline says 1–2 h after the end of infusion) and a **trough** (within ~30 min before next dose),
  ideally at or near steady state (~4th dose), same dosing interval.

## 3. Two-level worked calculation (linear PK)
1. Ke = ln(C1/C2) / Δt (C1 = peak, C2 = trough, Δt = hours between draws). t½ = 0.693/Ke.
2. Back-extrapolate: Cmax (end of infusion) = C1 / e^(−Ke·t_after_infusion);
   Cmin (true trough) = C2 · e^(−Ke·t_before_dose).
3. AUC infusion phase ≈ t_inf × (Cmax + Cmin)/2 ; AUC elimination phase = (Cmax − Cmin)/Ke.
4. AUC_tau = sum; **AUC24 = AUC_tau × 24/tau**.
5. Adjust (linear kinetics): new daily dose = current daily dose × (target AUC / measured AUC).
   Change interval if t½ suggests the current one is wrong.
*Example (illustrative):* 1,250 mg q12h, peak 30 mg/L at 1 h post 1-h infusion, trough
12 mg/L drawn 9 h later → Ke = ln(30/12)/9 ≈ 0.102 h⁻¹, t½ ≈ 6.8 h, AUC24 roughly 480 (recomputed: 484)
mg·h/L → in range. Recompute with your own times — sample timing errors dominate.

## 4. Recheck, AKI and special populations
- Re-level at least weekly in stable patients (guideline rec: once-weekly for hemodynamically stable patients), and **promptly** with changing renal function,
  haemodynamic instability, or concomitant nephrotoxins (piperacillin–tazobactam, aminoglycosides, loop diuretics, contrast).
- AKI (creatinine up ≥0.3 mg/dL or ≥50% (gated: unconfirmed, source is paywalled or blocked)): hold or reduce, recheck level, consider alternative agent.
- **Obesity:** load on actual weight; maintenance often lower per kg — level early.
- **Haemodialysis/CRRT, ECMO, burns, augmented renal clearance, pediatrics/neonates:**
  use specialist protocols; pediatric empiric regimens are higher mg/kg/day and need
  local guideline verification.

## Gotchas
- **Trough-only monitoring** to 15–20 mg/L is no longer recommended for serious MRSA; a trough is a poor AUC surrogate.
- Wrong documented sample times are the commonest TDM error — confirm actual infusion start/stop and draw times on the MAR.
- Drawing the "trough" after the next dose has started.
- Non-serious infections (e.g. uncomplicated skin infection) may not need AUC targeting — follow local policy.
- Oral vancomycin (C. difficile) is not absorbed — no TDM.

## Verify
- [ ] Loading dose on actual body weight for serious infection; infusion rate safe.
- [ ] Levels drawn with recorded real times; method (Bayesian or two-level) stated.
- [ ] AUC24 calculated and in 400–600 (or local target); adjustment documented.
- [ ] Renal function and nephrotoxic co-medications reviewed at each recheck.
- [ ] Special-population cases referred to protocol/specialist and doses verified locally.
