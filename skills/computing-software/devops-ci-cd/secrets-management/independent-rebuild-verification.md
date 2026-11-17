---
id: computing-software.devops-ci-cd.secrets-management.independent-rebuild-verification
name: independent-rebuild-verification
category: computing-software
field: devops-ci-cd
product: secrets-management
tags: [secrets-management, independent-rebuild, rebuilderd, reproducible-builds, diffoscope, build-verification, slsa-l4]
level: practitioner
status: draft
description: "Verify release artifacts by rebuilding them independently: reproducibility prerequisites, rebuilderd, digest comparison, diffoscope triage and CI double builds."
sources:
  - https://reproducible-builds.org/docs/
  - https://github.com/kpcyrd/rebuilderd
  - https://diffoscope.org/
  - https://reproducible-builds.org/docs/source-date-epoch/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Independent rebuild verification

A signature proves who published an artifact; an independent rebuild proves the artifact matches the source. If two builders on separate infrastructure produce bit-identical output, compromising one build system isn't enough to ship a backdoor.

## Prerequisite: reproducibility
Sources of non-determinism to remove:
- Timestamps: honour `SOURCE_DATE_EPOCH` (set from the last commit time `git log -1 --format=%ct`); `tar --mtime=@$SOURCE_DATE_EPOCH --sort=name --owner=0 --group=0 --numeric-owner`; `gzip -n`.
- File order: sorted inputs to archivers and linkers.
- Paths: `-ffile-prefix-map=$PWD=.` (C/C++), `-trimpath` (Go), `--remap-path-prefix` (Rust).
- Locale/timezone: `LC_ALL=C TZ=UTC`.
- Toolchain: pinned compiler and dependency versions (lockfiles, container image by digest).
- Build IDs and random seeds: Go `-buildvcs=false` or consistent VCS state; `-Wl,--build-id=sha1` deterministic.

## Double build in CI (cheap first step)
```yaml
jobs:
  build:
    strategy: { matrix: { runner: [ubuntu-24.04, ubuntu-22.04] } }
    runs-on: ${{ matrix.runner }}
    steps:
      - uses: actions/checkout@v4
      - run: make dist && sha256sum dist/* > sums-${{ matrix.runner }}.txt
      - uses: actions/upload-artifact@v4
        with: { name: sums-${{ matrix.runner }}, path: sums-*.txt }
  compare:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - uses: actions/download-artifact@v4
      - run: diff <(cut -d' ' -f1 sums-ubuntu-24.04/*) <(cut -d' ' -f1 sums-ubuntu-22.04/*)
```
`reprotest` varies environment (time, user, umask, locale, build path) between two builds automatically.

## Truly independent rebuilds
- Run the rebuild on infrastructure controlled by a different team or party (another cloud account, a volunteer rebuilder).
- rebuilderd: schedules rebuilds of distro packages (Arch, Debian, Tails) and publishes results; you can run your own instance for your packages.
- Publish build inputs needed for rebuilding: buildinfo (Debian `.buildinfo`), SLSA provenance listing builder image digest and parameters.
- Go modules: checksum database (sum.golang.org) gives tamper-evidence for sources; rebuild binaries with the same Go version to compare.

## When digests differ
```bash
diffoscope --html diff.html a/app.tar.gz b/app.tar.gz
```
diffoscope recurses through archives, ELF, jars, PDFs and shows exactly which bytes differ (embedded timestamp, path, ordering).

## Policy
- Gate releases on a matching rebuild for high-assurance artifacts; otherwise publish the rebuild status.
- Track reproducibility as a test: a change that breaks it fails CI.

## Verify
- [ ] Two builds in different environments give identical sha256 for every release artifact.
- [ ] A rebuild from published provenance by a second party matches the released digest.
