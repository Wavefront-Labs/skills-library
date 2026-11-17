---
id: computing-software.systems-network-administration.nix.nix-shell-dev-environment
name: nix-shell-dev-environment
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, nix-shell, pure-shell, shellhook, ad-hoc-packages]
level: practitioner
status: docs-checked
description: "Start a build or ad hoc development shell with nix-shell: -p packages, --pure, --run versus --command, shellHook, NIX_BUILD_SHELL and pinning nixpkgs."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/command-ref/nix-shell.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`nix-shell` builds a derivation's dependencies (not the derivation itself), sets its environment variables and sources `$stdenv/setup`. With no path it uses `shell.nix` if present, else `default.nix`.

```
nix-shell '<nixpkgs>' --attr hello
nix-shell -p sqlite libX11
nix-shell --pure --command 'echo hi'
nix-shell -p hello -I nixpkgs=<tarball-url> --run hello
```

Options:
- `--command <cmd>`: run in an interactive shell then exit; end with `return` to stay.
- `--run <cmd>`: non-interactive, so Ctrl-C exits.
- `--pure`: clears most of the environment (`HOME`, `USER`, `DISPLAY` are kept); `--keep <name>` preserves named variables.
- `--packages` / `-p`: Nixpkgs attributes or expressions such as `git.override { ... }`.
- `--exclude <regexp>`: skip dependencies whose store paths match.

Environment: `NIX_BUILD_SHELL` selects the session shell (default `bashInteractive` from `<nixpkgs>`, else `bash`); `NIX_PATH` determines where `-p` finds Nixpkgs; `-I nixpkgs=...` overrides.

`shellHook`, if defined by the derivation, runs after `$stdenv/setup`, only in `nix-shell`.

In a shell for a package, run build phases with `eval ${phase:-phase}` (for example `unpackPhase`) so overridden phases are respected.

## Checked

2026-11-04: default path, options, --pure behaviour, NIX_BUILD_SHELL, shellHook, -p expressions, -I override and the eval phase idiom confirmed against the nix-shell manual page. Removed nothing.

Method: documentation only; no commands were run.
