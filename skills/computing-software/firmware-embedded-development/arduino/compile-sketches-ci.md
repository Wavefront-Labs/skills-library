---
id: computing-software.firmware-embedded-development.arduino.compile-sketches-ci
name: compile-sketches-ci
category: computing-software
field: firmware-embedded-development
product: arduino
tags: [arduino-cli, arduino-ci, compile-sketches, github-actions, size-deltas, arduino-lint, arduino, firmware-embedded-development]
level: practitioner
status: docs-checked
description: "Set up GitHub Actions CI for Arduino sketches and libraries with arduino/compile-sketches: board matrix, library sources, warnings and memory-size delta reports on pull requests."
sources:
  - https://github.com/arduino/compile-sketches/blob/main/README.md
  - https://github.com/arduino/report-size-deltas/blob/main/README.md
  - https://github.com/arduino/arduino-lint-action/blob/main/README.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# compile-sketches CI

`arduino/compile-sketches` is Arduino's official GitHub Action. It installs cores and libraries
with arduino-cli, compiles every sketch for every board you list, and can record flash/RAM
usage so pull requests show size changes.

## Workflow
```yaml
# .github/workflows/compile.yml
name: Compile examples
on: [push, pull_request]

jobs:
  compile:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        board:
          - fqbn: arduino:avr:uno
            platforms: |
              - name: arduino:avr
          - fqbn: esp32:esp32:esp32
            platforms: |
              - name: esp32:esp32
                source-url: https://espressif.github.io/arduino-esp32/package_esp32_index.json
    steps:
      - uses: actions/checkout@v4
      - uses: arduino/compile-sketches@v1
        with:
          fqbn: ${{ matrix.board.fqbn }}
          platforms: ${{ matrix.board.platforms }}
          libraries: |
            - source-path: ./            # the library under test (repo root)
            - name: Stepper
              version: 1.1.3
          sketch-paths: |
            - examples
          enable-warnings-report: true
          enable-deltas-report: true
          sketches-report-path: sketches-reports
      - uses: actions/upload-artifact@v4
        with:
          name: sketches-reports-${{ strategy.job-index }}
          path: sketches-reports
```
- `sketch-paths` searches recursively for sketches.
- `libraries` accepts registry names (with optional `version`), `source-path` (local
  directory) and `source-url` (git repo or zip) entries.
- `cli-compile-flags` is a YAML list of extra `arduino-cli compile` flags, e.g. `- --warnings=all`
  (see the compile command reference for the flags).
- Pin platform and library versions so CI failures mean your change broke something, not an
  upstream release.

## Size deltas on pull requests
A second workflow runs `arduino/report-size-deltas@v1` from a scheduled workflow
(recommended for public repositories) and comments the memory-usage change on the pull request, using
the uploaded artifacts whose names match `sketches-reports-source` (regular expression, default
`sketches-reports`).

## Library repos: also lint
```yaml
      - uses: arduino/arduino-lint-action@v1
        with:
          library-manager: update      # or "submit" before first registry submission
          compliance: strict
```
Catches `library.properties` errors, missing examples and naming problems before the Library
Manager indexer rejects a release.

## Verify
- [ ] Every example compiles on every supported board in CI, with warnings reported.
- [ ] Size-deltas comment appears on a test PR.
- [ ] Versions of cores and libraries pinned in the workflow.

## Checked

Date: 2026-10-25. Documentation release: README files on the default branches (compile-sketches latest commit 2026-10-14).

Confirmed: inputs `fqbn`, `platforms`, `libraries` (name/version, source-path, source-url), `sketch-paths` (default examples, searched recursively), `cli-compile-flags` (YAML list), `enable-deltas-report`, `enable-warnings-report`, `sketches-reports-source` default `sketches-reports` (a regular expression matched against artifact names); report-size-deltas runs from a scheduled workflow; arduino-lint-action `library-manager` values submit, update, false and `compliance: strict`. Fixed: the artifact name in the example did not match the default `sketches-reports-source`; `workflow_run` is not documented and was removed; the example library version was not from a document.

Method: documentation only; no commands were run.
