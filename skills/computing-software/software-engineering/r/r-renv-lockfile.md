---
id: computing-software.software-engineering.r.r-renv-lockfile
name: r-renv-lockfile
category: computing-software
field: software-engineering
product: r
tags: [r, r-reproducibility, renv-lockfile]
level: practitioner
status: draft
description: "Pin package versions per project with renv and rebuild them from renv.lock."
sources: ["https://cran.r-project.org/manuals.html", ""]
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# renv init, snapshot and restore
- `renv::init()` creates a project library, `renv.lock` and `.Rprofile`; `renv::snapshot()` records installed versions; `renv::restore()` reinstalls them.
- Commit `renv.lock`, `.Rprofile`, `renv/activate.R` and `renv/settings.json`; ignore `renv/library`.
- `renv::status()` shows drift; `renv::update()` upgrades; `renv::install("pkg@1.2.3")` pins a version.
- Record the R version in docs; `sessionInfo()` in reports.
Verify: `renv::restore()` in a clean checkout and run tests.
