---
id: natural-sciences.chemistry.gaussian.optimisation-and-frequency-jobs
name: optimisation-and-frequency-jobs
category: natural-sciences
field: chemistry
product: gaussian
tags: [gaussian, gaussian16, g16, gaussview, quantum-chemistry, input-file, route-section, opt-freq, geometry-optimisation, frequency-calculation, link0, nprocshared, mem, chk, checkpoint, charge-multiplicity, scf-convergence, scf-xqc, opt-calcfc, maxcycles, imaginary-frequency, transition-state, ts-search, thermochemistry, zero-point-energy, gibbs-free-energy, scrf-smd, empiricaldispersion-gd3bj, slurm]
level: practitioner
status: docs-checked
description: "Write and debug a Gaussian opt+freq job: route section, charge/multiplicity, Link 0, SCF and geometry convergence failures, imaginary frequencies, reading thermochemistry."
sources: ["https://gaussian.com/opt/", "https://gaussian.com/freq/", "https://gaussian.com/scf/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Gaussian optimisation and frequency jobs

**Goal:** a converged minimum (or transition state) with frequencies and
thermochemistry from Gaussian 16, and a routine for the usual failures.

## 1. Input file anatomy
```
%nprocshared=16
%mem=32GB
%chk=mol.chk
#p opt freq b3lyp/def2svp empiricaldispersion=gd3bj scrf=(smd,solvent=dichloromethane) int=ultrafine

Title line: what this job is

0 1
C   0.000000   0.000000   0.000000
...
<blank line — required at the end>
```
- **Link 0** (`%`): cores and memory must match your queue request; set %mem a bit
  *below* what the scheduler gives (Gaussian's memory plus overhead).
- **Route** (`#p` = verbose output): method/basis, job types, options.
- **Charge multiplicity**: `0 1` neutral singlet; radicals `0 2`; triplets `0 3`. Wrong
  multiplicity is the most common silent error. Open-shell: Gaussian uses UHF/UKS
  automatically for multiplicity > 1; check ⟨S²⟩ for spin contamination.
- The file must end with a blank line; missing it causes cryptic end-of-file errors.
- Functional/basis choice: see natural-sciences.chemistry.computational-chemistry.dft-functional-and-basis-set-selection.

## 2. When the SCF won't converge
In order of escalation:
1. Better starting geometry (pre-optimise with a cheap method/basis, read with `guess=read geom=check`).
2. `scf=(maxcycle=512)`; `scf=xqc` (adds an extra quadratic-convergence step if the first-order SCF fails).
3. `scf=yqc` for very large molecules; for metals, check the initial guess (`guess=mix` for
   broken-symmetry singlets; fragment guesses for complexes).
4. Check that charge/multiplicity are physically sensible.

## 3. When the optimisation won't converge
- "Number of steps exceeded": restart from the last geometry with
  `opt=(maxcycles=200) geom=allcheck guess=read` (or repeat the route with `opt=restart`).
- Oscillating energies: compute the initial Hessian `opt=calcfc` (or `calcall` for
  very floppy/hard cases); flat potential surfaces may benefit from a finer integration grid.
- Use a smaller step size: `opt=(maxstep=10)`.

## 4. Frequencies
- **Must be at the same level of theory** as the optimisation (same functional, basis,
  solvent, grid) — otherwise the thermochemistry is meaningless.
- Minimum: 0 imaginary frequencies. One small imaginary frequency often means a
  loose optimisation or grid noise: tighten the optimisation and grid, displace
  along the mode and re-optimise.
- **Transition state:** `opt=(ts,calcfc,noeigentest)` from a good guess; confirm exactly 1 imaginary
  frequency whose animation is the bond change you expect; run an IRC to prove it
  connects the right minima.

## 5. Reading the output
- Thermochemistry block: "Sum of electronic and thermal Free Energies" = G at
  298.15 K, 1 atm by default (change with the `Freq` temperature/pressure options). Energies in hartree.
- Low-frequency modes inflate entropy; apply quasi-harmonic corrections externally
  (e.g. GoodVibes) for flexible molecules, and add the 1 atm → 1 M standard-state correction for solutions.

## Gotchas
- `%chk` files are binary and version-specific; `formchk` makes a portable .fchk.
- State the Gaussian version used; defaults differ between versions.

## Checked
2026-11-01. Confirmed on the Gaussian Opt page (MaxCycles, MaxStep, Restart, CalcFC, NoEigenTest), SCF page (XQC adds an extra QC step; YQC for very large molecules; MaxCycle) and Freq page (defaults 298.15 K, 1 atm; free-energy line in the output). Removed: the ultrafine-default claim, the 50i threshold, IRC option values, 627.5 conversion, GaussView steps, symmetry and scratch-disk notes (not confirmed).

Method: documentation only; no commands were run.

## Verify
- [ ] Normal termination and four "YES" convergence criteria on the last optimisation step.
- [ ] Frequencies at the same level; 0 imaginary (minimum) or 1 (TS, confirmed by IRC).
- [ ] ⟨S²⟩ acceptable for open-shell species.
- [ ] Free energies corrected for low modes and standard state where relevant.
- [ ] Input, output and checkpoint archived with the Gaussian version recorded.
