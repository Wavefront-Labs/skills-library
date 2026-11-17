---
id: computing-software.systems-network-administration.nix.flake-inputs-follows
name: flake-inputs-follows
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, follows, input-override, non-flake-input, flake-false]
level: practitioner
status: docs-checked
description: "Control flake inputs: non-flake inputs with flake = false, overriding transitive inputs, follows to dedupe nixpkgs, and self.submodules or self.lfs."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Input options in `flake.nix`:

- Non-flake inputs, for repositories without a `flake.nix`:

```
inputs.foo = { url = "github:owner/repo"; flake = false; };
```

- Override a transitive input:

```
inputs.nixops.inputs.nixpkgs = {
  type = "github";
  owner = "my-org";
  repo = "nixpkgs";
};
```

- Follow, reusing another input's dependency so only one copy is locked:

```
inputs.nixpkgs.follows = "dwarffs/nixpkgs";
```

- Self attributes `inputs.self.submodules` and `inputs.self.lfs` control how this flake is fetched when used as an input.

(Owner and repo above are the manual's placeholders; the `follows` target is the manual's example.)

`follows` and an override combine, for example `inputs.nixops.inputs.nixpkgs.follows = "dwarffs/nixpkgs";`. The manual notes it is generally not useful to eliminate transitive `nixpkgs` inputs this way, because most flakes provide overlays or NixOS modules that are composed into the top-level `nixpkgs`.

## Checked

2026-11-04. Confirmed against the Nix flake manual page: `flake = false` inputs, overriding a transitive input, `follows` as a `/`-separated path of input names, `inputs.self.submodules` and `inputs.self.lfs` (both default false), and the combined override and follows example. Replaced an override line the manual does not show with the manual's form, and removed an unsourced lock-file gotcha and a `nix flake metadata` verify line.

Method: documentation only; no commands were run.
