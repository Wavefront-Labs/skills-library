---
id: computing-software.software-engineering.fortran.fortitude
name: fortitude
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, fortitude, fortran-tooling]
level: practitioner
status: draft
description: "Lint Fortran with Fortitude, which checks style and correctness rules from the command line."
sources:
  - https://github.com/fortran-lang/fprettify
  - https://github.com/PlasmaFAIR/fortitude
  - https://github.com/fortran-lang/fortls
  - https://forddocs.readthedocs.io/
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# fortitude linter
**Goal:** catch common mistakes statically.
```bash
pip install fortitude-lint        # or pipx / uv; package name per project docs
fortitude check src/
fortitude explain <rule>          # show a rule explanation (verify subcommand in docs)
```
- Fortitude is a fast Fortran linter written in Rust by PlasmaFAIR, modelled on Ruff.
- Rules cover missing `implicit none`, missing `intent`, obsolescent features, style.
- Configure with `fpm.toml` `[extra.fortitude]` or `fortitude.toml` (unconfirmed key layout; consult docs).
- Run in CI and pre-commit.
## Gotchas
- Rule codes change as the project evolves; pin the version.
- Package name on PyPI should be confirmed in the project README before installing.
## Self-check
Remove an `implicit none` and confirm Fortitude reports it.
