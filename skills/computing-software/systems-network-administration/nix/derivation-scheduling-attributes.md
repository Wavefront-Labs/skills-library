---
id: computing-software.systems-network-administration.nix.derivation-scheduling-attributes
name: derivation-scheduling-attributes
category: computing-software
field: systems-network-administration
product: nix
tags: [nix, prefer-local-build, allow-substitutes, required-system-features, impure-env-vars]
level: advanced
status: docs-checked
description: "Steer where and how a derivation builds with preferLocalBuild, allowSubstitutes, requiredSystemFeatures and impureEnvVars."
sources:
  - https://raw.githubusercontent.com/NixOS/nix/master/doc/manual/source/language/advanced-attributes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Build scheduling attributes on a derivation:
- `preferLocalBuild`: when `true`, prefers building locally. Useful when a local build is cheapest.
- `allowSubstitutes`: when `false`, Nix always builds the derivation instead of substituting its outputs.
- `requiredSystemFeatures`: restricts building to machines whose `system-features` include all listed features, for example `"kvm"`.

Impure builder configuration:
- `impureEnvVars`: lists environment variables passed from the calling user's environment into the builder.

Example fragment:

```
requiredSystemFeatures = [ "kvm" ];
preferLocalBuild = true;
allowSubstitutes = false;
```

Use `requiredSystemFeatures` together with remote builders: a builder entry must advertise the feature in `system-features` for the build to be dispatched there.

Example from the manual: `fetchurl` in Nixpkgs lists `http_proxy` and `https_proxy` in `impureEnvVars` so it uses the proxy configured by the user.

## Checked

2026-11-04. Confirmed against the Nix manual Advanced Attributes page: `preferLocalBuild`, `allowSubstitutes`, `requiredSystemFeatures` with `system-features`, and `impureEnvVars` with the `fetchurl` proxy example. Removed an unsourced reproducibility gotcha and a `nix-store --query --binding` verify line.

Method: documentation only; no commands were run.
