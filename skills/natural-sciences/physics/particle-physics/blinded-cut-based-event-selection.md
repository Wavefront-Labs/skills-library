---
id: natural-sciences.physics.particle-physics.blinded-cut-based-event-selection
name: blinded-cut-based-event-selection
category: natural-sciences
field: physics
product: particle-physics
tags: [particle-physics, hep, event-selection, cut-based-analysis, blinding, blind-analysis, signal-region, control-region, sideband, cutflow, monte-carlo, simulation, background-estimation, abcd-method, figure-of-merit, punzi, significance, s-over-sqrt-b, look-elsewhere-effect, unblinding, collider, lhc, atlas, cms, lhcb, neutrino-physics, systematic-uncertainty]
level: advanced
status: verified
description: "Design a blinded cut-based event selection: define signal region, optimise cuts on simulation and sidebands, control regions, cutflow, and unblinding rules."
sources: ["J. R. Klein & A. Roodman, Blind Analysis in Nuclear and Particle Physics, Annu. Rev. Nucl. Part. Sci. 55 (2005)", "G. Punzi, Sensitivity of searches for new signals, arXiv:physics/0308063", "G. Cowan et al., Asymptotic formulae for likelihood-based tests, arXiv:1007.1727"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Blinded cut-based event selection

**Goal:** a selection that isolates a signal from backgrounds, whose choices were
fixed *before* anyone looked at data in the signal region, so the result can't be
tuned (consciously or not) toward the answer you hoped for.

## 1. Define the regions before optimising anything
- **Signal region (SR):** where signal is expected, e.g. a mass window around the
  hypothesised peak or a high-score region of a classifier. This is what stays blind.
- **Control regions (CR):** enriched in each major background and nearly free of signal;
  used to normalise or validate background models.
- **Validation regions (VR):** between CR and SR in the extrapolated variable; used to
  test the background extrapolation without touching the SR.
- Write these down (internal note, analysis twiki/repo) with the date. The blinding
  policy itself — what is hidden, who can lift it — is agreed with the review group.

## 2. Optimise on simulation and sidebands only
- Start from preselection driven by trigger and object quality (trigger plateau,
  object ID, overlap removal) — keep these *outside* the optimisation loop.
- Choose a figure of merit that matches the goal:
  - discovery: Asimov significance Z = √(2[(s+b)ln(1+s/b) − s]) — better than
    s/√b when b is small (s=5, b=0.5: Z=4.05 vs s/√b=7.07; at b=100 both ≈0.5). A toy-MC median of √q0 for s=5, b=1 matched the Asimov formula (3.39);
  - unknown signal strength / exclusion: Punzi FOM ε_s / (a/2 + √b), a = desired number of σ (e.g. 3 or 5); Punzi 2003, arXiv:physics/0308063, eq. 7.
- Scan cuts with simulation for signal and with simulation or data *sidebands* for
  background. Avoid optimising on fluctuations: require a healthy number of expected background MC events after cuts (a handful is noise: the "optimum" then tracks fluctuations).
- Prefer few, physically motivated cuts. Each extra cut adds a systematic and a
  place where data/MC disagree.

## 3. Background estimate
- Normalise dominant backgrounds in CRs (transfer factor CR→SR from simulation),
  or use a fully data-driven method such as ABCD with two uncorrelated variables:
  N_A = N_B·N_C/N_D. **Check the correlation** of the two variables in simulation
  and in the VR; ABCD is wrong if they are correlated (toy test, cuts at 1σ: independent variables predicted 5010 vs 5063 true in A; correlation 0.5 predicted 2475 vs 12529 true), and the residual becomes a systematic.
- Keep a **cutflow table** (events after each cut, data vs. expected) for every
  region. A cut where data/MC suddenly diverges points at a mismodelled variable.

## 4. Systematics before unblinding
Include detector (energy scale/resolution, efficiencies, pile-up), theory
(cross-sections, PDF, scale variations) and background-method uncertainties. Fix
the statistical model (likelihood, nuisance parameters) and produce **expected**
limits/significance with Asimov data. Pull and impact plots on CR-only fits should
show no nuisance pulled far beyond ±1σ.

## 5. Unblinding
- Unblind only after the review signs off the frozen selection, the background model
  and the expected sensitivity.
- After unblinding, **do not change cuts** to chase an excess or deficit. Bugs found
  afterwards are fixed and documented, with both results shown.
- For a peak scanned over mass, quote local and global significance (look-elsewhere effect).

## Gotchas
- Using data in the SR "just to check the trigger" is unblinding.
- Machine-learning scores trained on simulation can learn generator artefacts; check
  score distributions in CRs.
- Tiny MC statistics in the tail: weight fluctuations from a few large-weight events
  can dominate; check effective event counts.
- *Uncertainty note:* blinding conventions differ by collaboration (ATLAS, CMS, LHCb,
  neutrino experiments); follow your group's documented policy over this outline.

## Verify
- [ ] SR/CR/VR definitions and FOM were recorded before optimisation.
- [ ] No SR data entered any plot or table before sign-off.
- [ ] Background method validated in VRs; ABCD variables shown uncorrelated.
- [ ] Expected results and nuisance-parameter pulls reviewed pre-unblinding.
- [ ] Post-unblinding changes, if any, are documented with before/after numbers.
