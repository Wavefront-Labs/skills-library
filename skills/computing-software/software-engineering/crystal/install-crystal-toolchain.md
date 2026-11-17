---
id: computing-software.software-engineering.crystal.install-crystal-toolchain
name: install-crystal-toolchain
category: computing-software
field: software-engineering
product: crystal
tags: [install-crystal-toolchain, getting-started, install, crystal-version, homebrew, apt, snap, llvm, shards, crystal]
level: intro
status: draft
description: "Install Crystal and shards via package manager, installer script or tarball, and check the version and LLVM it was built with."
sources:
  - https://crystal-lang.org/reference/
  - https://crystal-lang.org/api/
  - https://github.com/crystal-lang/shards
  - https://crystal-lang.org/docs/
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Install the Crystal toolchain

Goal: get a working `crystal` and `shards` on PATH.

- macOS: `brew install crystal`. Linux: use the distro repo, the official OBS repository or a release tarball from the GitHub releases page (confirm current instructions on the install page). Windows: official zip or installer (check current support status).
- Verify with `crystal --version`; it prints the Crystal version, the LLVM version and the default target.
- `crystal env` shows CRYSTAL_PATH, CRYSTAL_CACHE_DIR and CRYSTAL_LIBRARY_PATH.
- Needs a C toolchain and libs (gcc or clang, libssl, libyaml, libgmp, libpcre2, libevent, libz) for full stdlib linking.

Gotchas:
- Missing dev libs show up as linker errors, for example `cannot find -lssl`.
- Distro packages can lag several minor versions; pin the version in CI.
- The cache lives under the user cache directory; clear it if odd stale-build behaviour appears.

Verify: `echo 'puts 1+1' | crystal eval` prints 2.
