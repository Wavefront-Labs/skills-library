---
id: computing-software.cloud-infrastructure-engineering.site-reliability-engineering.hermetic-and-reproducible-builds
name: hermetic-and-reproducible-builds
category: computing-software
field: cloud-infrastructure-engineering
product: site-reliability-engineering
tags: [hermetic-build-setup, reproducible-build-verification, release-engineering, bazel, reproducible-builds, supply-chain]
level: advanced
status: docs-checked
description: "Make release builds hermetic (pinned tools and dependencies, isolated from the host) and verify reproducibility by building twice and comparing artifact hashes."
sources: ["https://sre.google/sre-book/release-engineering/", "https://bazel.build/basics/hermeticity", "https://reproducible-builds.org/docs/", "https://slsa.dev/spec/v1.0/requirements"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Hermetic and reproducible builds

SRE Book (Release Engineering): builds must be hermetic, insensitive to the libraries and software installed
on the build machine, so that building the same revision always yields the same output. That makes
rollback and cherry-pick builds trustworthy, and release branches with cherry picks get their tests re-run.

## Hermetic build checklist (Bazel hermeticity page)
- **Isolation**: treat tools as source. Download copies of compilers and tools and keep them in managed
  file trees, so the host's installed versions do not matter.
- **Source identity**: identify inputs by a hash (a Git revision), and pin dependency versions.
- **No host leakage**: system binaries that differ across hosts, absolute paths and writes to the
  source tree are common sources of non-hermeticity.
- **Config too**: the SRE Book applies the same principle to configuration, packaging config files
  with the binary and rebuilding from the build ID.

## Reproducibility killers
The Reproducible Builds documentation has a page for each: `SOURCE_DATE_EPOCH`, timestamps, timezones,
locales, archive metadata, stable order for inputs and outputs, randomness, build path, version information.
Bazel's page adds build IDs and timestamps created non-deterministically. Look up the fix for your
toolchain on those pages rather than copying flags from memory.

## Verification
Bazel's troubleshooting advice: run each build step twice or on different systems, compare a hash of the
file contents, and treat differing results as not reproducible; also build inside a container holding only
the checked-out source and an explicit list of host tools so implicit system dependencies fail loudly.
Run this in CI on release tags and fail the release on mismatch. Record provenance for the artifact (see SLSA
requirements) and deploy by digest.

## Gotchas
- "Works in CI" builds that fetch the latest of anything are not hermetic even if they pass.
- Build tools themselves must be pinned; an unpinned plugin breaks hermeticity.
- Cherry-pick release builds must use the original toolchain, not today's.

## Verify
- [ ] Two clean builds of a tag produce identical digests.
- [ ] Build succeeds in a container with only the source and declared tools.
- [ ] Deploy manifests reference artifacts by digest.

## Checked
2026-11-01. Confirmed in the SRE Book Release Engineering chapter (hermetic builds, configuration packaging, cherry-pick test re-runs), the Bazel hermeticity page (isolation, source identity, non-hermetic sources, build-twice-and-hash advice, container build) and the Reproducible Builds documentation index (topic pages named above). Removed: specific commands and flags for Go, Bazel, npm, pip, tar, Docker and C compilers, and the sample verification script, which no fetched page states.
Method: documentation only; no commands were run.
