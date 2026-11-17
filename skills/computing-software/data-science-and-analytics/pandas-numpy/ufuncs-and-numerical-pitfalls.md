---
id: computing-software.data-science-and-analytics.pandas-numpy.ufuncs-and-numerical-pitfalls
name: ufuncs-and-numerical-pitfalls
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [numpy-ufuncs, float-comparison, np-isclose]
level: practitioner
status: docs-checked
description: "Compare floats with np.isclose, understand its tolerance rules and use isnan and ufunc.accumulate."
sources:
  - https://numpy.org/doc/stable/reference/ufuncs.html
  - https://numpy.org/doc/stable/reference/generated/numpy.isclose.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Ufuncs and float care
```python
np.isclose(0.1 + 0.2, 0.3)                 # True; never use == on floats
np.isnan(a)                                # element-wise NaN test
np.maximum.accumulate(a)                   # running maximum via ufunc.accumulate
```
## Gotchas
- `isclose` computes `abs(a - b) <= atol + rtol * abs(b)` (defaults `rtol=1e-05`, `atol=1e-08`), so it is not symmetric in a and b.
- The default `atol` is not appropriate for values near or below 1e-8; for example `isclose(1e-9, 2e-9)` is True. Choose `atol` for your scale.
- NaN values compare unequal unless `equal_nan=True`.
## Verify
- [ ] Tolerances chosen for the data scale, not left at defaults by accident.

## Checked

Method: docs-checked 2026-11-09 against the NumPy ufuncs reference (isnan and accumulate listings) and the numpy.isclose reference page (read via text conversion). Dropped nanmean/nansum, errstate, isfinite masking, cumsum and the summation-precision claim, which those pages do not cover.
