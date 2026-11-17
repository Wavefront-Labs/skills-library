---
id: computing-software.devops-ci-cd.github-actions.matrix-context-and-include-only-matrices
name: matrix-context-and-include-only-matrices
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, include-only-matrix, matrix-context, matrix]
level: practitioner
status: verified
description: "Use the matrix context and include-only matrices to define explicit job combinations with per-leg fields, plus where matrix values can and cannot be referenced."
sources: ["https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/run-job-variations", "https://docs.github.com/en/actions/reference/workflows-and-actions/contexts#matrix-context"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# matrix context and include-only matrices

## Include-only matrix
With no other keys, `include` becomes the full list of jobs. Each entry is one leg with arbitrary
fields:
```yaml
strategy:
  matrix:
    include:
      - { name: linux, os: ubuntu-24.04, target: x86_64-unknown-linux-gnu }
      - { name: mac-arm, os: macos-15, target: aarch64-apple-darwin }
      - { name: windows, os: windows-2025, target: x86_64-pc-windows-msvc, ext: .exe }
runs-on: ${{ matrix.os }}
name: build (${{ matrix.name }})
steps:
  - run: cargo build --release --target ${{ matrix.target }}
  - run: echo "artifact=app${{ matrix.ext }}" >> "$GITHUB_OUTPUT"
```
Missing fields (`ext` on linux) evaluate to empty string.

## include rules when other keys exist
For each include entry: if it matches existing combos without overwriting an original value, its
extra keys are **added** to those combos; if it cannot be added, a **new** combo is created. Common
surprise: an include whose key overwrites an original matrix value creates a new job instead of
modifying one.

## Where matrix is usable
- Yes: `runs-on`, `name`, `container`, `services`, `env`, `steps`, `timeout-minutes`,
  `continue-on-error`, job-level `concurrency`, `with:` of reusable calls.
- No: `jobs.<id>.if` (evaluated before the matrix is applied; actionlint reports `context "matrix" is not allowed here`).
- Job `outputs` values may use `matrix`, but all legs write the same output name and the last leg to run
  overrides the others (order is not guaranteed). Give each leg a unique output name
  (for example `output_${{ matrix.version }}`) and GitHub combines them.
- `toJSON(matrix)` in a step prints the leg, handy for debugging.

## Gotchas
- Leg names in required checks: set `name:` explicitly so renaming a field does not rename checks.
- A matrix can generate at most 256 jobs per workflow run (GitHub-hosted and self-hosted).

## Verify
- [ ] Job list shows exactly one job per include entry with the expected names.
