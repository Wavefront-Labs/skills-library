---
id: computing-software.systems-network-administration.nix.lang-lookup-paths
name: lang-lookup-paths
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, lookup-path, nix-path, find-file, path-literals]
level: practitioner
status: docs-checked
description: "Understand Nix lookup paths like <nixpkgs>: they resolve through builtins.nixPath, and differ from path literals, which need a slash."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/constructs/lookup-path.md
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/syntax.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A lookup path has the form `<identifier>` or `<identifier/subpath>`. It resolves to a path value when the identifier matches an entry in `builtins.nixPath`, the search path setting. `builtins.findFile` documents the full resolution algorithm.

Examples:

```
<nixpkgs>
<nixpkgs/nixos>
```

On a channel-based system these resolve to paths under `/nix/var/nix/profiles/per-user/root/channels/nixpkgs`.

Path literals are different: a path needs at least one slash, so `foo` is not a path but `./foo` is. Paths can start with `~` for the home directory, which is disallowed in pure evaluation. Absolute paths make expressions less portable.

## Checked

2026-11-04. Confirmed against the Nix manual Lookup path and Language Constructs pages: the `<identifier>` syntax, resolution through `builtins.nixPath`, the two channel examples, and the path literal rules (a slash is required, `~` and pure evaluation, absolute paths less portable). Removed unsourced `nix-instantiate`, `-I` and `NIX_PATH` command lines, a reproducibility gotcha, and a verify line.

Method: documentation only; no commands were run.
