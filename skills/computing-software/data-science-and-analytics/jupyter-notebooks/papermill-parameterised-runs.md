---
id: computing-software.data-science-and-analytics.jupyter-notebooks.papermill-parameterised-runs
name: papermill-parameterised-runs
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [papermill-parameters, parameters-cell, batch-notebook-run, jn-execution-conversion]
level: practitioner
status: docs-checked
description: "Tag a parameters cell and execute notebooks from the CLI or Python with injected parameters, producing a separate output notebook per run."
sources:
  - https://papermill.readthedocs.io/en/latest/usage-parameterize.html
  - https://papermill.readthedocs.io/en/latest/usage-execute.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# papermill
Tag one cell `parameters` with default values (Notebook: View > Cell Toolbar > Tags; JupyterLab 3+: property inspector > Add Tag).
```bash
papermill report.ipynb out/report_EU.ipynb -p region EU -p alpha 0.6
papermill report.ipynb out.ipynb -f params.yaml
papermill report.ipynb out.ipynb -r version 1.0
```
```python
import papermill as pm
pm.execute_notebook("report.ipynb", "out.ipynb", parameters=dict(alpha=0.6, ratio=0.1))
```
## Gotchas
- Papermill inserts a new cell tagged `injected-parameters` immediately after the `parameters` cell, containing only the overridden parameters. With no `parameters` cell it goes at the top of the notebook.
- The `parameters` cell holds defaults; derived values in it are not recomputed. With `a = 1` and `twice = a * 2`, running `-p a 9` gives `a = 9` and `twice = 2`, not 18. Compute derived values in a later cell.
- `-p` values that look like booleans or numbers are interpreted as such; `-r` (`--parameters_raw`) keeps the value a string.
- Other CLI inputs: `-f` (`--parameters_file`) takes a YAML file, `-y` a YAML string, `-b` a base64-encoded YAML string. YAML allows arrays and dictionaries.
- Only the first cell tagged `parameters` is the parameters cell; later cells with that tag are treated as normal cells.
- A comment `#papermill_description=NAME` at the start of a cell labels it in the progress bar; it must contain no spaces.
## Verify
- [ ] Output notebook shows the injected-parameters cell with the intended values.

## Checked

2026-11-09. Confirmed against the papermill Parameterize and Execute pages: tagging steps, injected-parameters placement, the inter-dependent parameters caveat, -p/-r/-f/-y/-b options, execute_notebook call, cell descriptions. Removed: the kernel_name argument, the claim that failed runs leave a traceback in the output notebook, and the dated output filename convention (not on the pages).
Method: docs-checked 2026-11-09 against the papermill Parameterize and Execute pages.
