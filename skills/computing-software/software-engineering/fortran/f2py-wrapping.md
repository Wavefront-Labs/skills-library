---
id: computing-software.software-engineering.fortran.f2py-wrapping
name: f2py-wrapping
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, f2py-wrapping, fortran-interop-python]
level: practitioner
status: draft
description: "Wrap Fortran routines for Python with numpy f2py, using intent annotations and column-major arrays."
sources:
  - https://numpy.org/doc/stable/f2py/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# f2py wrapping for Python
**Goal:** expose Fortran to Python.
```bash
python -m numpy.f2py -c -m fastmod fastmod.f90
```
```python
import numpy as np, fastmod
a = np.asfortranarray(np.random.rand(1000, 1000))
fastmod.scale(a, 2.0)
```
- Dummy `intent(in/out/inout)` determines the Python signature; `intent(out)` becomes a return value; `intent(inout)` arguments are modified in place only if the array is Fortran-contiguous.
- Use `!f2py intent(...)` comments to override.
- Check the f2py docs for the current build backend (newer NumPy versions use meson for the build; unconfirmed per version).
## Gotchas
- A C-ordered NumPy array triggers a copy; use `order='F'`.
- Module procedures appear as attributes `fastmod.mod.func`.
## Self-check
Call from Python and compare with a NumPy reference result.
