---
id: computing-software.systems-network-administration.nix.nix-build-basics
name: nix-build-basics
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-build, result-symlink, out-link, dry-run]
level: intro
status: docs-checked
description: "Build a Nix expression with nix-build: default.nix lookup, tarball URLs, the result symlink as a GC root, --out-link, --no-out-link and --dry-run."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-build.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-build` builds the derivations from the given expressions and, on success, creates a `result` symlink in the current directory (`result-2` and so on for further paths). With no path it uses `default.nix`. A path starting with `http://` or `https://` is a tarball URL, downloaded and unpacked; it must contain a single top-level directory holding a `default.nix`. It wraps `nix-instantiate` and `nix-store --realise`.

```
nix-build '<nixpkgs>' --attr firefox
nix-build --dry-run '<nixpkgs>' --attr firefox
nix-build --expr 'with import <nixpkgs> {}; runCommand "foo" {} "echo bar > $out"'
nix-build -o my-link '<nixpkgs>' --attr hello
```

Options:
- `--dry-run`: show what would be built or downloaded.
- `--out-link` / `-o`: name the symlink instead of `result`.
- `--no-out-link`: no symlink, so the output is not a GC root and `nix-store --gc` may collect it.
- `--arg` and `--attr`/`-A` go to `nix-instantiate`; other options go to `nix-store --realise`.

Warning: the result is a garbage collector root, and that root disappears if the `result` symlink is deleted or renamed.

## Checked

2026-11-04. Confirmed against the Nix manual nix-build page: the `result` and `result-2` symlinks, the `default.nix` default, tarball URL rules, the wrapper of `nix-instantiate` and `nix-store --realise`, `--dry-run`, `--out-link` and `-o`, `--no-out-link`, option routing, the `--expr` example and the garbage collector root warning. Removed an unsourced verify line.

Method: documentation only; no commands were run.
