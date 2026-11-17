---
id: computing-software.data-science-and-analytics.jupyter-notebooks.clean-notebooks-in-git
name: clean-notebooks-in-git
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [nbstripout, jupytext-pairing, notebook-diff, jn-reproducibility]
level: practitioner
status: docs-checked
description: "Strip outputs on commit with nbstripout and pair notebooks with plain-text scripts via jupytext for reviewable diffs."
sources:
  - https://github.com/kynan/nbstripout
  - https://github.com/mwouts/jupytext
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Notebooks in git
```bash
pip install nbstripout jupytext
nbstripout --install                    # git filter that strips outputs and some metadata
jupytext --set-formats ipynb,py:percent notebook.ipynb
jupytext --sync notebook.ipynb
```
## Gotchas
- Stripping outputs removes cached results from commits (they stay on disk); keep a rendered export (HTML) for sharing.
- `nbstripout --install` configures the repository's git filter; git does not set it up on clone, so every contributor runs it. Add `--attributes .gitattributes` to record the attribute in a committed file. Flags such as `--keep-count` and `--keep-output` relax what is stripped.
- Paired files: jupytext loads inputs from the most recent paired file, so edit one side at a time.
- Never commit notebooks containing credentials in outputs or cells.
## Verify
- [ ] `git diff` on a re-run notebook shows only code changes.

## Checked
Confirmed from the nbstripout README: it strips output and some metadata, works as a git filter, `--install`, `--install --attributes .gitattributes`, `--keep-count`, `--keep-output`, and that clones do not install the filter automatically. Confirmed from the jupytext README: `--set-formats ipynb,py:percent`, `--sync`, the `py:percent` format, and inputs loaded from the most recent paired file. Removed: claim that execution counts are removed by the filter was reduced to "some metadata" wording plus the documented `--keep-count` flag. The jupytext readthedocs site returned an empty page, so the GitHub README was read instead.
Method: docs-checked 2026-11-09 against the nbstripout README (GitHub page, install and options sections) and the jupytext README (raw GitHub text, full).
