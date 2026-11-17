---
id: computing-software.data-science-and-analytics.pandas-numpy.broadcasting-rules
name: broadcasting-rules
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [broadcasting-rules, newaxis-reshape, axis-reductions, np-broadcasting]
level: practitioner
status: docs-checked
description: "Predict output shapes with the broadcasting rules, use newaxis and keepdims, and pick the right axis for reductions."
sources:
  - https://numpy.org/doc/stable/user/basics.broadcasting.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Broadcasting
Rule: NumPy compares shapes from the trailing (rightmost) dimension leftwards; two dimensions are compatible when they are equal or one of them is 1. Otherwise it raises `ValueError: operands could not be broadcast together`.
```python
a = np.array([0.0, 10.0, 20.0, 30.0])   # shape (4,)
b = np.array([1.0, 2.0, 3.0])           # shape (3,)
a[:, np.newaxis] + b                    # (4,1) + (3,) -> (4,3)
```
## Gotchas
- `np.newaxis` inserts a new axis, so `a[:, np.newaxis]` turns shape (4,) into (4, 1); both arrays are then stretched to (4, 3).
- Inputs do not need the same number of dimensions.
## Verify
- [ ] Predict the result shape by hand (right to left) before running; an incompatible pair raises `ValueError`.
## Checked
2026-11-02. Confirmed against the NumPy "Broadcasting" user guide: the trailing-dimension rule, the equal-or-1 rule, the ValueError, and the `np.newaxis` example. Removed: `keepdims`/axis-reduction examples, the ddof note and the memory note (not stated on that page).
Method: documentation only; no commands were run.
