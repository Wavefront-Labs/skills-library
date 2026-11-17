---
id: engineering-technology.aerospace-engineering.ansys-fluent.fluent-journals-and-pyfluent-automation
name: fluent-journals-and-pyfluent-automation
category: engineering-technology
field: aerospace-engineering
product: ansys-fluent
tags: [fluent, ansys, fluent-postprocessing, fluent-journals, tui, pyfluent, automation, batch-processing, scripting]
level: advanced
status: draft
description: "Automate Fluent with journal files, TUI commands and the PyFluent Python API for repeatable setups, angle-of-attack sweeps and batch post-processing."
sources:
  - "Ansys Fluent TUI command reference"
  - "PyFluent (ansys-fluent-core) documentation"
  - "Fluent user guide (journal files)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
aliases: []
---

# Fluent journals and PyFluent

**Goal:** reproducible, scriptable runs.

## Journals and TUI
- Record: **File > Write > Start Journal**; stop with Stop Journal. Journals contain TUI commands.
- Run headless: `fluent 3ddp -g -t8 -i run.jou` (3D double precision, no graphics, 8 processes, journal input).
- Typical commands: `/file/read-case-data case.cas.h5`, `/solve/iterate 500`, `/file/write-case-data out.cas.h5`, `/exit yes`.

## PyFluent
```python
import ansys.fluent.core as pyfluent
solver = pyfluent.launch_fluent(mode="solver", precision="double", processor_count=8)
solver.file.read_case_data(file_name="case.cas.h5")
solver.solution.run_calculation.iterate(iter_count=500)
```
Names of settings objects follow the Fluent GUI and TUI; check the installed version's documentation, since the settings API changed between releases.

## Alpha sweep pattern
Loop over alpha: set far-field flow direction and the lift and drag vectors, iterate, write forces to a CSV, continue from the previous solution.

## Gotchas
- Journals are version-sensitive; test after upgrades.
- Always add `/exit yes` and write logs so batch runs end cleanly.
- Use absolute or relative paths set in the script, not machine-specific paths in shared journals.

## Verify
- [ ] Re-running the journal on a clean session reproduces the same forces.
