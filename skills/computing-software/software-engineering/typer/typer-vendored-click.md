---
id: computing-software.software-engineering.typer.typer-vendored-click
name: typer-vendored-click
category: computing-software
field: software-engineering
product: typer
tags: [typer, click, vendoring, migration, compatibility, dependencies]
level: advanced
status: docs-checked
description: "Typer 0.26.0 vendors Click: what breaks (extracting the Click app, Click types and plug-ins), why dependency conflicts disappear, and how to migrate."
sources:
  - https://github.com/fastapi/typer/blob/master/docs/tutorial/click.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Vendored Click in Typer

Historical background, only needed if you maintain apps that touched Click directly.

## What changed

Typer used to depend on Click as an external package. Since **version 0.26.0** Typer vendors Click: a copy of Click's source code is included inside Typer, with unified interactions between Typer and that embedded code.

## Breaking change

Typer used to let you:

- extract the internal Click app from a Typer app, to modify it with Click functionality (for example Click-specific plug-ins);
- add Click-specific types to override Typer's default ones.

That edge-case feature is **no longer supported**, and some other Click functionality will disappear over time. If your app depended on it, either migrate it to plain Typer or migrate it to use Click directly instead of Typer.

## Why it helps you

Many packages ship a CLI, some on Click and some on Typer, all living in one project. Previously a package needing a newer Click than Typer supported would force an install that broke the Typer-based one, or pins made some combinations uninstallable. Now a package can depend on a newer Click while a Typer-based package keeps working, because that Typer version bundles whatever it needs from Click.

It also frees both teams: Typer no longer needs workarounds for new Click releases, and Click does not need to consider Typer-caused edge cases.

## What comes next

Typer will reduce, simplify and refactor the vendored code it does not need, then gradually add long-planned features that were too hard before. Trade-offs were weighed against real use cases from the official Typer developer survey.

## Migration checklist

1. Search your code for use of the Click app extracted from a Typer app, Click plug-ins, or Click types passed into Typer.
2. If found, decide: rewrite using plain Typer features, or move that CLI to Click directly.
3. Do not assume Click behaviours stay available in future Typer releases.

## Checked

2026-11-07. Read in full against click.md (Typer docs repository checkout). Confirmed: vendoring since 0.26.0, breaking change, dependency conflict explanation, planned simplification, developer survey. Removed or trimmed: nothing removed.

Method: documentation only; no commands were run.
