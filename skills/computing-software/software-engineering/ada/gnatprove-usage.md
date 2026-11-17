---
id: computing-software.software-engineering.ada.gnatprove-usage
name: gnatprove-usage
category: computing-software
field: software-engineering
product: ada
tags: [ada, gnatprove-usage]
level: practitioner
status: docs-checked
description: "Run gnatprove modes (check, check_all, flow, prove, all), --level, --prover, -j, --report and read unproved check messages."
sources:
  - https://docs.adacore.com/spark2014-docs/html/ug/
  - https://learn.adacore.com/courses/intro-to-spark/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Running gnatprove and reading results
```
gnatprove -P proj.gpr --mode=flow
gnatprove -P proj.gpr --level=2 -j0 --report=all
gnatprove -P proj.gpr -u file.adb --limit-line=file.adb:42
```
- Output lists each check (overflow, range, index, division) as proved or "might fail".
- `--mode` values: check, check_all (stone), flow (bronze, the default in GNAT Studio), prove, all, silver, gold.
- `--level=0..4` are presets (0 fastest: cvc5, timeout 1; 4 strongest: timeout 60); an explicit `--prover`, `--timeout` or `--steps` overrides the level. Levels are not reproducible across machines; use `--steps` or `--replay` for shared builds.
- `-j0` uses all cores; unchanged units are not reanalyzed unless you pass `-f`.
- Proved checks are printed only with `--report=all|provers|statistics`.
- Session and result files live in the `gnatprove` subfolder of the root project object directory.
## Gotchas
- A passing flow stage does not imply proof; run prove mode too.
## Self-check
Run on a function with `A + B` and no bounds; expect an unproved overflow check ("overflow check might fail").

## Checked
2026-11-03. Confirmed in the SPARK User's Guide (running GNATprove, viewing output): `--mode` values, `--level` presets and override rule, `-j0`, `-u`, `--limit-line`, `-f`, `--report` values, "might fail" message form, `gnatprove` subfolder. Removed `--clean` (not documented on the pages read) and the claim that flow/prove are alone sufficient.
Method: documentation only; no commands were run.
