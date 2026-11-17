---
id: computing-software.data-science-and-analytics.pandas-numpy.random-generator-reproducibility
name: random-generator-reproducibility
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [default-rng, random-seed-reproducibility, bootstrap-resample]
level: practitioner
status: docs-checked
description: "Use numpy.random.default_rng with explicit seeds and spawned streams for reproducible sampling, shuffling and bootstrap resampling."
sources:
  - https://numpy.org/doc/stable/reference/random/index.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Random Generator
```python
rng = np.random.default_rng(42)
rng.random()
rng.integers(low=0, high=10, size=5)
```
## Gotchas
- NumPy recommends `Generator` (created with `default_rng`) over the older `RandomState` and the functions in `numpy.random`; they are not scheduled for removal.
- Generators are deterministic sequences that can be reproduced by specifying a seed.
- For parallel work, read the "Parallel Applications" section (SeedSequence spawning, independent streams, jumping) of the NumPy random documentation rather than sharing one generator.
## Verify
- [ ] Re-running with the same seed gives identical output.
## Checked
2026-11-02. Confirmed against the NumPy "Random sampling" index page: `default_rng`, `Generator.random`, `Generator.integers`, seed reproducibility, the RandomState note, and the parallel-applications options. Removed: `normal`, `choice`, the bootstrap loop and the `SeedSequence.spawn()` call (not shown on that page).
Method: documentation only; no commands were run.
