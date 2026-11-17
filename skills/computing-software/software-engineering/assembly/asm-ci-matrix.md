---
id: computing-software.software-engineering.assembly.asm-ci-matrix
name: asm-ci-matrix
category: computing-software
field: software-engineering
product: assembly
tags: [assembly, asm-ci-matrix, asm-containers-ci]
level: practitioner
status: draft
description: "Continuous integration for assembly across architectures: GitHub Actions matrix over x86-64 and arm64 runners, feature-gated tests, artifact checks and QEMU fallback."
sources:
  - https://sourceware.org/binutils/docs/binutils/
  - https://refspecs.linuxfoundation.org/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# CI matrix for x86-64 and arm64
**Goal:** run the same test-suite on each architecture and OS you ship.

```yaml
name: ci
on: [push, pull_request]
jobs:
  test:
    strategy:
      fail-fast: false
      matrix:
        os: [ubuntu-latest, ubuntu-24.04-arm, macos-latest, windows-latest]
    runs-on: ${{ matrix.os }}
    steps:
      - uses: actions/checkout@v4
      - name: Toolchain (Linux)
        if: runner.os == 'Linux'
        run: sudo apt-get update && sudo apt-get install -y nasm binutils gcc
      - name: Build and test
        run: make test
      - name: Inspect output
        if: runner.os == 'Linux'
        run: |
          readelf -n build/demo | grep -E 'IBT|SHSTK|BTI' || true
          readelf -lW build/demo | grep GNU_STACK
```
- Native arm64 runners exist on GitHub (for example the `ubuntu-24.04-arm` label and Apple-silicon `macos-latest`); availability depends on plan and repository visibility, so check current documentation. Fall back to `qemu-user` on x86 runners when native runners are not available.
- Make tests choose paths at run time by CPU features (see cpuid-feature-detect) and report which path ran, so CI logs show whether AVX2 or NEON code was exercised.
- Add static checks: `.note.GNU-stack` present, no text relocations (`readelf -d | grep TEXTREL`), expected stack non-executable.
- Cache toolchain downloads; keep jobs short so failing architectures report quickly.

## Gotchas
- Hosted runners vary in CPU model; features such as AVX-512 may be absent, so tests must skip rather than crash.
- Windows needs a different assembler and object format; give it its own build step.

## Self-check
Introduce a bug only on arm64 (wrong register) and confirm the matrix isolates it.
