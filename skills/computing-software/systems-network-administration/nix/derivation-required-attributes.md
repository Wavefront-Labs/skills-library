---
id: computing-software.systems-network-administration.nix.derivation-required-attributes
name: derivation-required-attributes
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, derivation, builtins-derivation, builder, outputs]
level: practitioner
status: docs-checked
description: "Create a store derivation with builtins.derivation: required name, system and builder, optional args and outputs, and how other attributes become environment variables."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/derivations.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `derivation` builtin makes a store derivation from an attribute set; evaluating it yields an attribute set and registers a store derivation as a side effect.

Required:
- `name` (string): symbolic name, appears in store paths.
- `system` (string): system type that can build it, for example `"x86_64-linux"` or `builtins.currentSystem`.
- `builder` (path or string): the executable, such as an absolute path like `/bin/bash`, a local file Nix copies into the store, or a file from another derivation.

Optional:
- `args` (list of strings), default empty.
- `outputs` (list of strings), default `[ "out" ]`. Each output name is passed to the builder as an environment variable holding that output's store path. The output's store path name is the derivation name plus the output name, except `out`. The first output is the default; select others by attribute, such as `.dev`.

Other attributes become builder environment variables: strings unchanged, numbers in decimal, `true` as `1`, `false` and `null` as empty string, paths copied to the store, derivations built and replaced by their default output path, lists joined with spaces.

Example:

```
derivation {
  name = "hello";
  builder = "/bin/sh";
  args = [ "-c" "echo -n hello > $out" ];
  system = builtins.currentSystem;
}
```

## Checked

2026-11-04. Confirmed against the Nix manual Derivations page: required `name`, `system`, `builder`; optional `args` (default empty) and `outputs` (default `[ "out" ]`); output naming, default output and attribute selection; and the environment variable conversion rules. Removed an unsourced verify line.

Method: documentation only; no commands were run.
