---
id: computing-software.data-science-and-analytics.pandas-numpy.ndarray-creation-dtypes
name: ndarray-creation-dtypes
category: computing-software
field: data-science-and-analytics
product: pandas-numpy
tags: [ndarray-creation, numpy-dtypes, arange-linspace, np-arrays]
level: intro
status: docs-checked
description: "Create arrays with array, zeros, arange and linspace and pick dtypes deliberately to avoid overflow and silent float conversion."
sources:
  - https://numpy.org/doc/stable/user/basics.creation.html
  - https://numpy.org/doc/stable/user/basics.types.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# ndarray creation
```python
import numpy as np
a = np.array([1, 2, 3], dtype=np.int64)
np.zeros((3, 4)); np.ones(5)
np.arange(0, 10, 2); np.linspace(0, 1, 11)
a.dtype, a.shape, a.ndim
```
## Gotchas
- Casting to a fixed-width type can overflow: converting an int64 300 to int8 gives 44 (NumPy follows C casting rules).
- `np.arange` with a float step can include the stop value because of roundoff error; `np.linspace` makes a specified number of elements spaced equally between the start and end values.
- `numpy.int_` and `numpy.intp` have platform-dependent sizes; prefer explicit bit-sized dtypes for file formats and low-level code.
## Verify
- [ ] Print dtype and shape after each creation; check bounds with `np.iinfo(np.int8)`.
## Checked
2026-11-02. Confirmed against NumPy "Array creation" and "Data types" user guides: `zeros`, `ones`, `arange`, `linspace`, the roundoff note, overflow example (300 to 44), platform-dependent integer sizes and `np.iinfo`. Removed: `np.full`, `nbytes`, and the "integer arrays overflow silently" claim (reworded to the documented casting case).
Method: documentation only; no commands were run.
