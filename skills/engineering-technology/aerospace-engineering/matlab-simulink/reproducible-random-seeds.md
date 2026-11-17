---
id: engineering-technology.aerospace-engineering.matlab-simulink.reproducible-random-seeds
name: reproducible-random-seeds
category: engineering-technology
field: aerospace-engineering
product: matlab-simulink
tags: [matlab, simulink, monte-carlo-dispersions, monte-carlo, dispersions, seed-reproducibility, rng, random-streams, band-limited-white-noise]
level: practitioner
status: docs-checked
description: "Make Monte Carlo and noise-driven Simulink runs reproducible with explicit random streams, per-run seeds, and independent streams on parallel workers."
sources:
  - https://www.mathworks.com/help/matlab/ref/rng.html
  - https://www.mathworks.com/help/matlab/ref/randstream.create.html
  - https://www.mathworks.com/help/simulink/slref/parsim.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
aliases: []
---

# Reproducible random seeds

**Goal:** the same results on rerun, different noise in different runs.

## Practice
- Set the MATLAB generator once at the start: `rng(12345, 'twister')`.
- Simulink random-source blocks take their own seed parameters: set each as a workspace variable and assign it per run through `Simulink.SimulationInput.setVariable`, for example `seedK = base + k`.
- Parallel workers: separate seeds are "not guaranteed to be statistically independent" per the `RandStream.create` page. For independence create streams with `RandStream.create('threefry', 'Seed', base, 'NumStreams', N, 'StreamIndices', k)`: streams made with the same generator, `Seed` and `NumStreams` and different `StreamIndices` (1 to `NumStreams`) belong to one group; or pre-generate all random draws on the client and pass them in.
- Store seeds and sample matrix with the results; rerun a single failing case by its seed.

## Gotchas
- `rng("default")` does not guarantee the same results across sessions with different settings; call `rng(seed, generator)` explicitly.

## Checked

2026-11-01. Confirmed on the MathWorks rng and RandStream.create pages: `rng(seed,generator)`, `"twister"`,
explicit generator recommended for stable results, `Seed`, `NumStreams`, `StreamIndices`, the `"threefry"` generator
name and independence conditions. Removed: the claim about `parsim` run order and worker draws, the block-seed
correlation claim and named Simulink noise blocks (not confirmed from docs).
Method: documentation only; no commands were run.

## Verify
- [ ] Two identical runs with the same seed table produce bit-identical outputs.
- [ ] Two different seeds produce different time histories.
