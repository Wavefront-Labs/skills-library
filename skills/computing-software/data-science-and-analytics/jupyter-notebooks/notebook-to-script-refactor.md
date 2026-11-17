---
id: computing-software.data-science-and-analytics.jupyter-notebooks.notebook-to-script-refactor
name: notebook-to-script-refactor
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [notebook-refactor, extract-functions-module, notebook-testing]
level: practitioner
status: draft
description: "Move reusable cells into an importable package with tests, leaving the notebook as a thin narrative that calls it."
sources:
  - https://docs.pytest.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# From notebook to code
1. Identify cells that are pure transformations; turn into functions with explicit inputs/outputs.
2. Move to `src/pkg/steps.py`; `pip install -e .`; import in the notebook (with `%autoreload 2`).
3. Add `pytest` tests with tiny fixture DataFrames.
4. Keep exploratory plots in the notebook, pipeline logic in the package.
## Gotchas
- Global variables from earlier cells are hidden inputs; make them parameters.
## Verify
- [ ] `pytest` passes and the notebook output is unchanged.
