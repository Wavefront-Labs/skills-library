---
id: computing-software.data-science-and-analytics.jupyter-notebooks.pin-environment-and-seeds
name: pin-environment-and-seeds
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [requirements-lock, random-seed-notebook, environment-capture]
level: practitioner
status: docs-checked
description: "Record exact package versions and set random seeds so a notebook reproduces its numbers on another machine."
sources:
  - https://pip.pypa.io/en/stable/cli/pip_freeze/
  - https://numpy.org/doc/stable/reference/random/generator.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Reproducible environment
```bash
python -m pip freeze > requirements.lock.txt
python -c "import sys; print(sys.version)"
```
```python
import random, numpy as np
random.seed(0); rng = np.random.default_rng(0)
```
First cell: print versions of the key libraries; read data from a path relative to the project, not an absolute local path.
## Gotchas
- `pip freeze` reports what is installed in requirements format; it is a snapshot, not a solver result or lockfile. By default it omits pip (and setuptools, wheel, distribute on Python 3.11 and earlier); `--all` includes them.
- `np.random.default_rng(seed)` does not manage a global instance: pass the `rng` object to code that needs randomness, and seed any other library's generator separately.
## Verify
- [ ] Fresh environment from the lock file reproduces key numbers.

## Checked
Confirmed on the pip freeze page: requirements-format output, the omitted bootstrap packages and `--all`, and that it is not a lockfile or solver. Confirmed on the NumPy page: `default_rng(seed)` is the recommended constructor and does not manage a default global instance. Removed: `pip-compile` and `conda env export --from-history` alternatives, the BLAS/hardware floating-point claim and the `random_state` advice, none of which the cited pages state.
Method: docs-checked 2026-11-09 against the pip freeze page (full) and the NumPy Generator and default_rng page (default_rng section).
