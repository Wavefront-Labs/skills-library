---
id: computing-software.devops-ci-cd.nx.nx-release-version-prefix
name: nx-release-version-prefix
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, nx-release, versionprefix, dependencies, package-json, semver]
level: practitioner
status: docs-checked
description: "Control the ^, ~, = or exact prefix nx release writes for dependency versions with the versionPrefix option; default auto preserves each existing prefix."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/guides/Nx%20Release/configuration-version-prefix.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: choose how nx release writes dependency version ranges in manifests (package.json, Cargo.toml, etc.) when it updates them.

Option: `release.version.versionPrefix`. Allowed values:
- `"auto"` (default): reuse the prefix already in the manifest.
- `""`: exact version, no prefix.
- `"~"`: patch-level compatibility.
- `"^"`: minor-level compatibility.
- `"="`: exact match lock (rare in JS, used by e.g. Cargo).

Auto example: with `"dependency-one": "~1.2.3"`, `"dependency-two": "^2.3.4"`, `"dependency-three": "3.0.0"`, the next patch of the dependency set gives `~1.2.4`, `^2.3.4`, `3.0.0`: each keeps its own prefix style.

Set it globally in `nx.json`, or per project in `project.json`:

```json
{ "release": { "version": { "versionPrefix": "^" } } }
```

With `^`, the guide's example shows dependencies written as `^1.0.0`, `^2.3.4` and `^3.0.0`.

A fixed prefix enforces a consistent approach to dependency ranges.

## Checked

2026-11-07. Confirmed against Configuring Version Prefix for Dependencies: versionPrefix default auto, the five values and their meanings, the auto example (~1.2.4, ^2.3.4, 3.0.0), setting it in nx.json or project.json, and the ^ example. Removed: advice on when to prefer a fixed prefix over auto (not on the page, replaced by the page's consistency remark), the invented -style ranges wording, and the invented dry-run Verify step.

Method: documentation only; no commands were run.
