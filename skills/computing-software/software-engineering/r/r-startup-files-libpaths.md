---
id: computing-software.software-engineering.r.r-startup-files-libpaths
name: r-startup-files-libpaths
category: computing-software
field: software-engineering
product: r
tags: [r, r-install-config, startup-files-libpaths]
level: practitioner
status: docs-checked
description: "Configure startup files, R_LIBS_USER and repos, and troubleshoot where packages install."
sources: ["https://stat.ethz.ch/R-manual/R-devel/library/base/html/Startup.html", "https://stat.ethz.ch/R-manual/R-devel/library/base/html/libPaths.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Rprofile, Renviron and library paths
- `?Startup` documents `Renviron.site` and `Rprofile.site` (under `R_HOME/etc`) as site-wide startup files, with user `.Renviron` and `.Rprofile` files as well.
- `R --vanilla` implies the options that skip site and user startup files (`?Startup`).
- `.libPaths()` gets or sets the library trees; the `R_LIBS` and `R_LIBS_USER` environment variables feed it (`?.libPaths`).
Verify: `.libPaths()` and `Sys.getenv("R_LIBS_USER")` show where packages are looked up.

## Checked

Date: 2026-11-02. Confirmed on: ?Startup (Renviron.site, Rprofile.site, --vanilla), ?.libPaths (R_LIBS_USER). Removed as not confirmed on those pages: The file read order, secrets advice, repos option, binary packages and Rtools claims (not read on these pages).

Method: documentation only; no commands were run.
