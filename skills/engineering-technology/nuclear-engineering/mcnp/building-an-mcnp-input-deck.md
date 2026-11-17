---
id: engineering-technology.nuclear-engineering.mcnp.building-an-mcnp-input-deck
name: building-an-mcnp-input-deck
category: engineering-technology
field: nuclear-engineering
product: mcnp
tags: [mcnp, mcnp6, monte-carlo, radiation-transport, input-deck, cell-cards, surface-cards, sdef, kcode, f4-tally, f5-point-detector, fmesh, mesh-tally, de-df-dose-functions, mode-n-p, importance, weight-windows, variance-reduction, statistical-checks, figure-of-merit, lost-particles, shannon-entropy, criticality, shielding, endf]
level: advanced
status: draft
description: "Build and debug an MCNP6.2/6.3 deck: cells, surfaces, materials, SDEF/KCODE sources, F2/F4/F5/FMESH tallies with DE/DF dose, importances, and passing the 10 statistical checks."
sources:
  - "MCNP6.2 User's Manual (LA-UR-17-29981)"
  - "MCNP6.3 User's Manual (LA-UR-22-30006)"
  - "MCNP Primer and Criticality Calculations Primer (LANL)"
  - "Shultis & Faw, An MCNP Primer"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building an MCNP input deck — from blank file to a converged, defensible tally

**Goal:** write an MCNP6.2/6.3 input that runs without lost particles, scores the quantity you actually need, and passes all ten statistical checks.

Engineering guidance only; results used in a safety basis need a qualified, independently reviewed model under your QA program. MCNP is export-controlled and licensed through RSICC.

## Deck structure

Title line, then cells, surfaces and data blocks separated by **single blank lines**. `&` continues a line, `$` starts an inline comment, `c ` starts a comment card.

```
Shielded Co-60 source, dose at 1 m
1  0          -1           imp:p=1      $ source void
2  1  -11.35   1 -2        imp:p=2      $ lead shell
3  2  -0.001205 2 -3       imp:p=4      $ air
4  0           3           imp:p=0      $ graveyard

1  so 2.0
2  so 7.0
3  so 150.0

mode p
m1  82000 1                             $ lead; photon library via default/PLIB
m2  7014 -0.755  8016 -0.232  18000 -0.013
sdef pos=0 0 0  erg=d1  par=2
si1 L 1.1732 1.3325
sp1   1      1
f5:p  100 0 0  0.5                      $ point detector, R0 exclusion radius
df5 iu=2 fac=1 ic=40                    $ built-in dose set (verify IC in manual)
nps 1e7
```

- Negative density = g/cm3, positive = atoms/(barn·cm); `-1` = inside surface 1.
- Every point must belong to exactly one cell; the outermost is `imp=0`.
- Pick libraries deliberately (`.80c` = ENDF/B-VII.1, `.00c` = ENDF/B-VIII.0). Add `MTn` S(alpha,beta) for bound hydrogen/graphite in thermal problems — omitting it biases k-eff.

## Sources

- **Fixed source (SDEF):** `POS`, `ERG`, `PAR`, `CEL`, `RAD`/`EXT`/`AXS` for volumes. Distributions via `SIn`/`SPn` (`L` lines, `H` histogram, `SP -3` Watt fission). Results are **per source particle**: scale by source strength with `FM` or in post-processing.
- **Criticality (KCODE):** `KCODE 20000 1.0 100 600` = histories/cycle, initial k guess, inactive cycles, total cycles, plus `KSRC` points (or `SDEF` spread across the fissile region). Inspect the **Shannon entropy** plot: inactive cycles must extend past where entropy stabilises, not just where k-eff looks flat.

## Tallies

| Tally | Scores | Units (per source particle) |
|---|---|---|
| F2 | surface-averaged flux | 1/cm2 |
| F4 | cell flux | 1/cm2 |
| F5 | point/ring detector flux | 1/cm2 |
| FMESH (6.x), TMESH | flux on a superimposed mesh | 1/cm2 |

`FMESH14:n GEOM=xyz ORIGIN=-50 -50 -50 IMESH=50 IINTS=20 JMESH=50 JINTS=20 KMESH=50 KINTS=20` gives a 20x20x20 map; pair with `DE14/DF14` to make it a dose map. For dose, use DE/DF pairs or the built-in `DFn IU= FAC= IC=` sets (ICRP-74 / ANSI/ANS-6.1.1 choices; confirm the IC numbers in your manual version). KCODE tallies are per fission neutron; scale with power, ν and Q.

## Variance reduction

- **Cell importances:** raise IMP by roughly a factor 2 per mean free path of shield so the particle population stays roughly constant; avoid jumps >4 between adjacent cells. Subdivide thick shields into slabs to allow this.
- **Weight windows:** generate with `WWG` (cell or `MESH`-based), iterate 2-3 times, run with `WWP` reading `wwout`. For deep penetration consider CADIS windows (ADVANTG).

## The ten statistical checks

Printed for one bin per tally (select it with `TFn`). All must pass:

1. Mean: no monotonic trend in the last half of the run.
2. Relative error R < 0.10 (< 0.05 for point detectors).
3. R decreases monotonically over the last half.
4. R falls as 1/sqrt(N) in the last half.
5. Variance of the variance VOV < 0.10.
6. VOV decreases monotonically.
7. VOV falls as 1/N.
8. Figure of merit FOM = 1/(R^2·T) roughly constant.
9. FOM shows no monotonic trend.
10. Slope of the largest-history-score tail ≥ 3 (finite second moment).

## Gotchas

- **Lost particles:** default run stops after 10. Plot geometry (`mcnp6 ip`); dashed lines mark gaps/overlaps. Debug with a `VOID` card and an inward flood source from a sphere outside the model; every lost particle then marks a gap or overlap. Raising the `LOST` limit is not a fix.
- Passing R < 0.1 but failing the slope test means a rarely sampled important path (e.g. a duct); improve sampling there rather than just running longer.
- Coupled `mode n p` needs photon-production data in the neutron library.

For criticality see engineering-technology.nuclear-engineering.reactor-physics.core-criticality-and-reactivity-coefficients; for hand cross-checks of shielding see engineering-technology.nuclear-engineering.radiation-shielding.point-kernel-shield-sizing.

## Verify

- [ ] Geometry plotted in three orthogonal planes with no dashed lines; zero lost particles in a VOID flood test.
- [ ] Densities, isotopics and library suffixes checked against the specification.
- [ ] All ten statistical checks pass for every tally bin used in the result.
- [ ] KCODE: Shannon entropy converged before the first active cycle; k-eff consistent across the three estimators.
- [ ] Per-source-particle tallies correctly scaled to physical source strength, with units stated.
- [ ] Result compared against a hand estimate or benchmark.
