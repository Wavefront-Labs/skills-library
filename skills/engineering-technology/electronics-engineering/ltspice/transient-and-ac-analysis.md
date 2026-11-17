---
id: engineering-technology.electronics-engineering.ltspice.transient-and-ac-analysis
name: transient-and-ac-analysis
category: engineering-technology
field: electronics-engineering
product: ltspice
tags: [ltspice, spice, circuit-simulation, transient-analysis, ac-analysis, bode-plot, tran, meas, step, monte-carlo, noise-analysis, loop-gain, phase-margin, stability, spice-model, subckt, include, op-amp-simulation, smps-simulation, analog-devices, ngspice]
level: practitioner
status: draft
description: "Simulate analog circuits in LTspice: .tran and .ac setup, .meas for numbers, .step for tolerance sweeps, loop gain/phase margin, and vendor model import."
sources:
  - "LTspice Help (built-in documentation of dot-commands and options), Analog Devices"
  - "Horowitz & Hill, The Art of Electronics, 3rd ed."
  - "Middlebrook, Measurement of loop gain in feedback systems (Int. J. Electronics, 1975)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# LTspice transient and AC analysis — numbers, not just pretty plots

**Goal:** answer a concrete design question (does it settle, is it stable, does it
survive tolerances) with LTspice simulations whose results are measured by `.meas`
and swept by `.step`, not eyeballed from one waveform.

## 1. Models first
- Use the vendor's model where one exists. Put the file next to the schematic and
  reference it with `.include opamp.lib` (subcircuits) or `.lib opamp.lib`. Avoid
  absolute paths so the project is portable.
- For a third-party `.subckt` with no symbol: open the `.lib`, right-click the
  `.subckt` line › *Create Symbol* (behaviour as in LTspice 17/24; check yours), or
  use a generic opamp symbol with `SpiceModel` set to the subckt name and pins in the
  model's order. **Pin order mismatch** is the most common silent error — read the
  `.subckt` header comment.
- Know what the model omits: many op-amp macromodels do not model noise, input
  common-mode limits or temperature drift. The datasheet still wins.

## 2. Transient (`.tran`)
Syntax: `.tran <Tstep> <Tstop> [Tstart [dTmax]] [startup|uic|steady]`.
- `.tran 0 20m 15m 100n` — run 20 ms, save only after 15 ms (skip start-up), cap the
  internal step at 100 ns. Set dTmax ≤ 1/50 of the fastest edge or period you care
  about; otherwise ringing and ripple are under-resolved.
- `startup` ramps sources from zero — good for regulators and converters.
- Add `.options plotwinsize=0` to disable waveform compression when measuring ripple
  or small errors; compression can hide detail.
- For SMPS, simulate long enough to reach steady state (soft-start plus a few
  hundred switching cycles) before measuring.

## 3. AC sweep (`.ac`)
- `.ac dec 100 1 1Meg` — 100 points/decade, 1 Hz to 1 MHz. The stimulus source must
  have an AC amplitude (`AC 1` in the source's Small Signal AC field).
- AC is linearised at the DC operating point: check `.op` first. If the op-amp output
  is railed in DC, the Bode plot is meaningless.

## 4. Loop gain and phase margin
Break the loop with a series voltage source at a point driven from low impedance
into high impedance (e.g. between the op-amp output `o` and the feedback network
node `fb`): source `+` on `fb`, `−` on `o`, value `AC 1`, DC 0. Then with T the loop
gain, `T = -V(o)/V(fb)`. Plot that expression:
```
.ac dec 200 10 100Meg
.meas AC fc WHEN mag(-V(o)/V(fb))=1
.meas AC pm FIND 180+ph(-V(o)/V(fb)) WHEN mag(-V(o)/V(fb))=1
```
`ph()` returns degrees in LTspice's measure output as I recall; if `pm` looks like
a radian value, convert. Target ≥45° (≥60° for well-damped steps). For loops where
the impedance condition isn't met, use the Middlebrook/Tian method (LTspice ships a
`LoopGain2` example demonstrating it).

## 5. Measure, don't squint (`.meas`)
```
.meas TRAN vpp PP V(out) FROM 15m TO 20m
.meas TRAN vavg AVG V(out) FROM 15m TO 20m
.meas TRAN trise TRIG V(out) VAL=0.1 RISE=1 TARG V(out) VAL=0.9 RISE=1
.meas AC g0 FIND mag(V(out)) AT 1k
.meas AC f3db WHEN mag(V(out))=g0/sqrt(2) FALL=1
```
For bandwidth, measure the passband reference first and refer to it (as above)
rather than hard-coding 0.707 — the passband gain is rarely exactly 1. Results appear in the
SPICE Error Log (View › SPICE Error Log, or Ctrl+L).

## 6. Sweeps and tolerances (`.step`)
- `.step param R1 1k 10k 1k`, `.step dec param C 1n 1u 5`, `.step list 2 5 10`.
- Monte Carlo: give parts `{mc(10k,0.01)}` (1 % uniform) and add `.step param run 1
  200 1`. Read `.meas` results across runs: in the error log window, right-click ›
  *Plot .step'ed .meas data*.
- `{gauss(x)}` and worst-case using `{wc(nom,tol)}` with a binary-counting step are
  common idioms; check the Help for exact distribution semantics.

## 7. Noise (`.noise`)
`.noise V(out) Vin dec 50 10 100k` then plot `V(onoise)`; integrate by Ctrl-click on
the trace label for total RMS over the plotted band. Only meaningful if the models
include noise sources.

## Gotchas
- Ideal sources and caps with zero ESR cause convergence trouble; add realistic
  series resistance (e.g. 10 mΩ ESR, 1 mΩ source R).
- "Time step too small": add small R/C damping, use `.options gmin=1e-10` sparingly,
  or try the alternate solver (Control Panel › SPICE). Don't paper over a genuinely
  oscillating circuit.
- Default `.tran` step can skip narrow pulses — always set dTmax for switching work.

## Verify
- [ ] `.op` shows every active device in its intended region before AC/transient.
- [ ] Key outputs are `.meas` statements, re-run after every change.
- [ ] Phase margin measured, not inferred from a step plot.
- [ ] A `.step`/Monte Carlo run shows the spec holds across tolerances.
- [ ] Simulation agrees with a hand calculation within a sensible margin.
