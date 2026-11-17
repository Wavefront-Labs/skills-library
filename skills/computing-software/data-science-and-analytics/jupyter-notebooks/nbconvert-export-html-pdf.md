---
id: computing-software.data-science-and-analytics.jupyter-notebooks.nbconvert-export-html-pdf
name: nbconvert-export-html-pdf
category: computing-software
field: data-science-and-analytics
product: jupyter-notebooks
tags: [nbconvert-html, nbconvert-execute, hide-code-cells]
level: practitioner
status: docs-checked
description: "Execute and export notebooks to HTML, Markdown or script, hiding code or inputs for stakeholder reports."
sources:
  - https://nbconvert.readthedocs.io/en/latest/usage.html
  - https://nbconvert.readthedocs.io/en/latest/config_options.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# nbconvert
```bash
jupyter nbconvert --to html --execute report.ipynb
jupyter nbconvert --to html --no-input report.ipynb         # hide code cells
jupyter nbconvert --to script report.ipynb
jupyter nbconvert --to markdown --output-dir out report.ipynb
```
## Gotchas
- Since nbconvert 6.0 there is no default format: always pass `--to`.
- PDF export (`--to pdf`) goes through LaTeX (and pandoc); `--to webpdf` uses Chromium via playwright (`nbconvert[webpdf]`). HTML is the dependable default.
- By default conversion aborts on a cell exception during `--execute`; `--allow-errors` continues and puts the error in the output. Use it only for debugging.
- Check the exported file for leaked secrets or private data in outputs.
## Verify
- [ ] Open the HTML and confirm no tracebacks.

## Checked
Confirmed on the nbconvert usage page: `--to html|markdown|script|pdf|webpdf`, `--execute`, `--allow-errors` behaviour, the 6.0 removal of the default format, LaTeX and pandoc dependency, webpdf needing playwright Chromium (`nbconvert[webpdf]`). Confirmed on the config options page: the `no-input` flag (sets `exclude_input`) and `output-dir` (FilesWriter.build_directory). Removed the unsupported phrase "or a Chromium-based route" in favour of the documented webpdf exporter.
Method: docs-checked 2026-11-09 against the nbconvert usage page (full) and the config options page (flag aliases section).
