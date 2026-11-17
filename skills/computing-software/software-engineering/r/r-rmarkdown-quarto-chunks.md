---
id: computing-software.software-engineering.r.r-rmarkdown-quarto-chunks
name: r-rmarkdown-quarto-chunks
category: computing-software
field: software-engineering
product: r
tags: [r, r-reports, rmarkdown-quarto-chunks]
level: practitioner
status: draft
description: "Render reports with knitr/Quarto, set chunk options and parameters and cache sensibly."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# R Markdown and Quarto chunk options
- Chunk options `echo`, `eval`, `include`, `message`, `warning`, `fig.width`, `fig.height`, `cache`; set defaults in a setup chunk `knitr::opts_chunk$set(...)`.
- Quarto uses `#| echo: false` comment-style chunk options and `quarto render file.qmd`; R Markdown uses `rmarkdown::render()`.
- Parameters via `params:` in the YAML header.
- Knitting runs in a fresh session with the document's directory as working directory; use `here::here()`.
- Caching can hide stale-data bugs.
Verify: render from a clean R session.
