---
id: computing-software.software-engineering.fortran.ci-github-actions
name: ci-github-actions
category: computing-software
field: software-engineering
product: fortran
tags: [fortran, ci-github-actions, fortran-containers-ci]
level: practitioner
status: draft
description: "Set up Fortran compilers in CI with the setup-fortran action, build and test with fpm or CMake, across compiler versions."
sources:
  - https://docs.docker.com/
  - https://github.com/fortran-lang/setup-fortran
  - https://fortran-lang.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Continuous integration on GitHub Actions
**Goal:** run tests on every push.
```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        compiler: [gcc]
        version: [13]
    steps:
      - uses: actions/checkout@v4
      - uses: fortran-lang/setup-fortran@v1
        with:
          compiler: ${{ matrix.compiler }}
          version: ${{ matrix.version }}
      - uses: fortran-lang/setup-fpm@v5
      - run: fpm test --profile release
```
- setup-fortran can install gcc (gfortran), intel (ifx), and other compilers across Linux, macOS, Windows (check the action README for supported values).
- Add jobs with `-fcheck=all` debug profile and a sanitizer run.
- Action version tags change; pin to a current major version after checking the repository.
## Gotchas
- Workflow versions in the example are indicative (unconfirmed current tags).
- Windows builds may need MSYS2 or the action's mingw setup.
## Self-check
Push a failing test to a branch and confirm the workflow goes red.
