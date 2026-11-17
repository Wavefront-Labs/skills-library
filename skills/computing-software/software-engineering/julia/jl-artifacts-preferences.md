---
id: computing-software.software-engineering.julia.jl-artifacts-preferences
name: jl-artifacts-preferences
category: computing-software
field: software-engineering
product: julia
tags: [julia, jl-artifacts-prefs, artifacts-preferences]
level: advanced
status: docs-checked
description: "Ship data and binaries with Artifacts.toml and store package settings with Preferences.jl."
sources: ["https://pkgdocs.julialang.org/v1/artifacts/", "https://docs.julialang.org/en/v1/manual/code-loading/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Artifacts.toml and Preferences.jl
- `Artifacts.toml` maps a name to a `git-tree-sha1` and download URLs; `artifact"name"` resolves to the local path of the unpacked artifact.
- `create_artifact` and `bind_artifact!` (Pkg.Artifacts API) create an artifact and record it in `Artifacts.toml`.
- Preferences are read and written through the Preferences.jl package and stored in `LocalPreferences.toml` next to the active project; a change to a preference read at compile time causes dependent code to be recompiled.
- Git-ignore `LocalPreferences.toml` unless the settings are meant to be shared.
Verify: delete the artifact cache and confirm it re-downloads.

## Checked

2026-11-02. Confirmed against: Pkg Artifacts page (Artifacts.toml keys, create_artifact, bind_artifact!) and manual Code Loading (Preferences, LocalPreferences.toml, git-ignore advice). Removed: the wrong key name git-tree-hash (the file uses git-tree-sha1), the lazy-download claim, the `_jll` aside and the `@load_preference` macro signature.
Method: documentation only; no commands were run.
