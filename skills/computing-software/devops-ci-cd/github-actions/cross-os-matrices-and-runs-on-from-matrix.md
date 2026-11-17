---
id: computing-software.devops-ci-cd.github-actions.cross-os-matrices-and-runs-on-from-matrix
name: cross-os-matrices-and-runs-on-from-matrix
category: computing-software
field: devops-ci-cd
product: github-actions
tags: [github-actions, matrix-os, cross-os-matrix, runs-on-matrix, windows-runner, macos-runner, path-separators, line-endings-autocrlf, shell-per-os, runner-os-conditionals, matrix-include-per-os, os-specific-steps, case-sensitive-filesystem, executable-extension, matrix, matrix-build]
level: practitioner
status: verified
description: "Run one job across Linux, Windows and macOS via runs-on matrix.os: force bash, fix path separators and CRLF, add per-OS include values, and skip steps with runner.os conditionals."
sources: ["https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/using-a-matrix-for-your-jobs#using-a-matrix-strategy", "https://docs.github.com/en/actions/using-github-hosted-runners/using-github-hosted-runners/about-github-hosted-runners#supported-runners-and-hardware-resources"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cross-OS matrices

**Goal:** one job definition that passes on all three OSes without a thicket of
`if: runner.os == ...` branches.

## 1. Skeleton
```yaml
jobs:
  test:
    strategy:
      fail-fast: false                     # see all OS failures, not just the first
      matrix:
        os: [ubuntu-24.04, windows-2022, macos-14]
        include:
          - os: ubuntu-24.04
            exe: ''
            cache-dir: ~/.cache/pip
          - os: windows-2022
            exe: .exe
            cache-dir: ~\AppData\Local\pip\Cache
          - os: macos-14
            exe: ''
            cache-dir: ~/Library/Caches/pip
    runs-on: ${{ matrix.os }}
    defaults: { run: { shell: bash } }     # Git Bash on Windows: forward slashes everywhere
    steps:
      - uses: actions/checkout@v4
      - run: ./build.sh && ./dist/app${{ matrix.exe }} --version
```
`include` entries that match an existing `os` leg **add** keys to it rather than creating a
new leg — the cleanest way to carry per-OS constants.

## 2. The five cross-OS traps
1. **Shell**: the default on Windows is `pwsh`; `shell: bash` there is the bash from Git for Windows
   (GitHub docs). Keep pwsh only for steps that need it.
2. **Line endings**: a script checked out with CRLF fails in bash with `^M` errors. Pin them with a
   `.gitattributes` rule (`*.sh text eol=lf`); verified locally with `git ls-files --eol`, which reports
   `w/lf attr/text eol=lf` even with `core.autocrlf=true`.
3. **Paths**: use `${{ runner.temp }}`/`$RUNNER_TEMP` and forward slashes; `path.join` in JS actions.
   Windows paths carry a drive letter (the docs' example `RUNNER_TEMP` is a `<drive>:` path ending in `\_temp`).
4. **Case-sensitivity**: code that only works on a case-insensitive filesystem (wrong-case import) will
   fail on the Linux leg.
5. **Executables**: Windows needs the `.exe` suffix. Use `matrix.exe` as above.

## 3. Per-OS steps
```yaml
      - if: runner.os == 'Linux'
        run: sudo apt-get install -y libfoo-dev
      - if: runner.os == 'macOS'
        run: brew install foo
      - if: runner.os == 'Windows'
        run: choco install foo -y
```
`runner.os` values are `Linux`, `Windows`, `macOS` (exact case). `matrix.os` is the label
string; prefer `runner.os` for conditionals so the matrix can change labels freely.

## 4. Cost and speed
GitHub bills hosted runners per minute at a rate that depends on OS and size (see the "Actions runner
pricing" reference; each job is rounded up to a whole minute), and macOS and Windows cost more than Linux.
Run the expensive legs only on the default branch or nightly (build the matrix with `fromJSON`) and cache
toolchains per OS (`key: ${{ runner.os }}-...`).

## Verify
- [ ] All three legs green with `fail-fast: false`.
- [ ] No `^M` or path errors in the Windows log.
- [ ] Cache keys include `runner.os`; hit rate per OS is non-zero.
