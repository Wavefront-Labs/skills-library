---
id: computing-software.systems-network-administration.nix.flake-nix-structure
name: flake-nix-structure
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, flake-nix, flake-outputs, nix-config, self-input]
level: practitioner
status: docs-checked
description: "Structure a flake.nix: description, inputs, outputs function, nixConfig, input metadata and the self input, with the manual's Hello example."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/src/nix/flake.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A `flake.nix` can contain:
- `description`: one-line summary.
- `inputs`: dependencies mapped to flake references.
- `outputs`: a function that receives the inputs and returns an attribute set of Nix values.
- `nixConfig`: `nix.conf` settings; only a small safe set applies without confirmation, such as `bash-prompt` and `flake-registry`.

Minimal example:

```
{
  description = "A flake for building Hello World";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-20.03";

  outputs = { self, nixpkgs }: {
    packages.x86_64-linux.default =
      with import nixpkgs { system = "x86_64-linux"; };
      stdenv.mkDerivation {
        name = "hello";
        src = self;
        buildPhase = "gcc -o hello ./hello.c";
        installPhase = "mkdir -p $out/bin; install -t $out/bin hello";
      };
  };
}
```

Each input passed to `outputs` also exposes `outPath`, `rev`, `revCount`, `lastModified`, `lastModifiedDate` and `narHash`. The special input `self` refers to this flake.

Evaluation: every input is fetched, evaluated and passed to `outputs` under its input name. `narHash` determines the store path, so inputs can come from a binary cache.

## Checked

2026-11-04. Confirmed against the Nix flake manual page: the supported `flake.nix` attributes, the Hello example, the input metadata attributes, the `self` input, the `nixConfig` allow-list (`bash-prompt`, `flake-registry` among others) and that each input is fetched, evaluated and passed to `outputs`. Removed an unsourced verify line.

Method: documentation only; no commands were run.
