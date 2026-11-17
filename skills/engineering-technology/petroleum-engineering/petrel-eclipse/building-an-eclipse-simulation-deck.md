---
id: engineering-technology.petroleum-engineering.petrel-eclipse.building-an-eclipse-simulation-deck
name: building-an-eclipse-simulation-deck
category: engineering-technology
field: petroleum-engineering
product: petrel-eclipse
tags: [eclipse, eclipse-100, e100, e300, petrel, opm-flow, reservoir-simulation, black-oil, simulation-deck, runspec, welspecs, compdat, wconprod, wconhist, history-matching, prt-file, convergence, summary-keywords, schedule-section, flow-simulator, slb]
level: advanced
status: draft
description: "Build and debug an Eclipse 100 black-oil deck: section order, key keywords, well/completion/control cards, Petrel export, PRT convergence triage and a history-match loop (OPM Flow compatible)."
sources:
  - "ECLIPSE Reference Manual and Technical Description (SLB, current release)"
  - "Petrel Reservoir Engineering user guide (SLB)"
  - "OPM Flow Reference Manual (Open Porous Media initiative)"
  - "Aziz & Settari, Petroleum Reservoir Simulation"
  - "SPE comparative solution projects (SPE1, SPE9, SPE10)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Building an Eclipse simulation deck — from Petrel grid to a converging, history-matched run

**Goal:** produce an Eclipse 100 (black-oil) `.DATA` deck that parses cleanly, converges with sensible timesteps and can be history-matched, whether written by hand or exported from Petrel.

## Section order and what lives where

Sections must appear in this order; optional ones in brackets.

| Section | Purpose | Key keywords |
|---|---|---|
| `RUNSPEC` | dimensions, phases, units, table sizes | `TITLE`, `DIMENS nx ny nz /`, `OIL`, `WATER`, `GAS`, `DISGAS`, `VAPOIL`, `METRIC`/`FIELD`, `TABDIMS`, `WELLDIMS`, `EQLDIMS`, `START`, `UNIFOUT` |
| `GRID` | geometry and static properties | `COORD`+`ZCORN` (corner point) or `DX/DY/DZ/TOPS`, `ACTNUM`, `PORO`, `PERMX/Y/Z`, `NTG`, `INIT` |
| [`EDIT`] | modify computed pore volumes/transmissibilities | `MULTX`, `TRANX`, `PORV` |
| `PROPS` | fluid and rock tables | `PVTO`/`PVDO`, `PVTW`, `PVDG`/`PVTG`, `DENSITY`, `ROCK`, `SWOF`, `SGOF` (or `SWFN/SOF3` family) |
| [`REGIONS`] | assign tables to cells | `SATNUM`, `PVTNUM`, `EQLNUM`, `FIPNUM` |
| `SOLUTION` | initial state | `EQUIL` (datum depth, pressure, OWC, Pc, GOC…), `RSVD`/`PBVD`, `RPTRST` |
| [`SUMMARY`] | vectors written to SMSPEC/UNSMRY | `FOPR`, `FWCT`, `FPR`, `WBHP`, `WOPR`, `WWCT`, `WGOR`, `ALL` |
| `SCHEDULE` | wells, controls, time | `WELSPECS`, `COMPDAT`, `WCONPROD`, `WCONINJE`, `WCONHIST`, `DATES`/`TSTEP`, `TUNING` |

Records end with `/`; a lone `/` closes a keyword with multiple records. `1*` defaults one item, `3*` three. Comments start with `--`; keep big arrays in `INCLUDE` files.

## Wells: the minimum working set

```
WELSPECS
 'P1' 'G1' 10 12 1* 'OIL' /
/
COMPDAT
-- well  I  J K1 K2 status sat CF   diam  Kh skin
 'P1'   10 12  3  8 'OPEN' 1*  1*  0.216  1*  0  /
/
WCONPROD
 'P1' 'OPEN' 'ORAT' 800 4* 50 /     -- 800 sm3/d oil target, 50 bar BHP limit
/
```

Default CF and Kh so Eclipse computes the Peaceman connection factor. For history match, replace `WCONPROD` with `WCONHIST` (observed ORAT/WRAT/GRAT, control mode usually `'RESV'` or `'ORAT'`) and `WCONINJH` for injectors; the simulator then honours rates and you match pressures and phase ratios.

## Petrel export

Use Petrel's Define Simulation Case: grid, properties, fluid model, rock physics functions, development strategy (well rules) and simulator choice. Export writes the `.DATA` plus `GRDECL`/include files. Before running, check `DIMENS` against the Petrel grid, that `ACTNUM` excludes zero-pore-volume cells, units are consistent (`METRIC` vs `FIELD`), and that the development strategy produced the `DATES` you expected.

## Debugging from the PRT file

Search the `.PRT` for `@--ERROR`, `@--PROBLEM`, `@--WARNING` in that order. Then:

1. **Initialisation:** compare FIP report in-place volumes with the static model (within ~1-2%). A big mismatch means `EQUIL` contacts, `PORO`/`NTG` or `ACTNUM` errors. Run one step with `NOSIM` in RUNSPEC to check initialisation fast.
2. **Initial equilibrium:** with no wells, pressures and saturations should not move. Drift means inconsistent `EQUIL`/`PVT`/`SWOF` endpoints (e.g. SWOF Swc ≠ `SWL` array) — use threshold `THPRES` or fix the tables.
3. **Convergence:** look for timestep chops (`CHOP`), many Newton iterations (>8-10 per step) and linear-solver failures. Typical culprits: tiny pore-volume cells (set `MINPV`/`MINPORV`), extreme permeability contrasts, non-monotonic PVT (Bo or Rs decreasing with pressure above Pb), relperm curves with vertical segments, wells completed in inactive cells.
4. `TUNING`: raise maximum step after events cautiously; do not "fix" convergence by loosening tolerances — that hides material-balance error.

## History-match workflow

1. Match field pressure (`FPR`, `WBHP`/RFT) first via pore volume, aquifer (`AQUFETP`/`AQUCT`) and compressibility.
2. Then water cut/GOR timing via relperm endpoints, `MULTX/MULTZ`, fault transmissibility and barriers.
3. Well-by-well last, with local multipliers only where geology supports them.
4. Track mismatch per well, use assisted history matching for ensembles, and log every change.

**OPM Flow** (open source, GPL) reads most Eclipse 100 keywords and writes Eclipse-format output (EGRID/UNRST/UNSMRY) readable by ResInsight and Petrel; SPE1/SPE9 decks run unmodified. Check its log for unsupported-keyword warnings. For decline-based cross-checks of forecasts, see engineering-technology.petroleum-engineering.reservoir-engineering.decline-curve-analysis-and-reserves; well lift constraints come from engineering-technology.petroleum-engineering.production-engineering.nodal-analysis-and-artificial-lift-selection (VFP tables via `VFPPROD`).

## Gotchas

- Item positions in `COMPDAT`/`WCONPROD` differ between keywords and versions; count defaults carefully — a misplaced `1*` silently sets a BHP limit as a rate.
- `WCONHIST` wells revert to their historical rate; in prediction you must switch to `WCONPROD` or they shut in when history ends.
- `FIELD` units use psia, stb/d, ft; mixing METRIC tables into a FIELD deck parses fine and is wrong.
- Petrel re-export overwrites hand edits; put edits in separate `INCLUDE` files.

## Verify

- [ ] Deck runs with zero `ERROR` and every `PROBLEM` explained.
- [ ] Initial in-place volumes match the static model within agreed tolerance.
- [ ] No-flow equilibrium run shows no pressure/saturation drift.
- [ ] Material-balance error reported in PRT is negligible (<0.1% typical).
- [ ] Newton iterations per step mostly below ~8 with few timestep chops.
- [ ] History-match plots (pressure, WCT, GOR) reviewed per well, changes logged.
