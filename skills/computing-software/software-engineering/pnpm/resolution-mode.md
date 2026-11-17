---
id: computing-software.software-engineering.pnpm.resolution-mode
name: resolution-mode
category: computing-software
field: software-engineering
product: pnpm
tags: [resolution-mode, time-based-resolution, lowest-direct, registry-supports-time-field, auto-dedupe, supported-architectures, optional-dependencies-setting, update-ignore-deps]
level: advanced
status: docs-checked
description: "Choose how pnpm picks versions: resolutionMode highest, time-based or lowest-direct, registrySupportsTimeField, autoDedupe, supportedArchitectures and update.ignoreDeps."
sources:
  - https://pnpm.io/settings/other
  - https://pnpm.io/settings/dependency-resolution
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`resolutionMode`:
- `highest` (default).
- `time-based`: direct dependencies resolve to their lowest versions; subdependencies resolve from versions published no later than one hour after the newest direct dependency (lowest satisfying version if none). With `minimumReleaseAge`, the earlier cutoff applies; `minimumReleaseAgeStrict` decides fallback. Needs full registry metadata, so it is slower unless `registrySupportsTimeField: true` (Verdaccio 5.15.1+, some proxies; also per registry via `supportsTimeField`).
- `lowest-direct`: only direct dependencies take the lowest version. Peers added by `autoInstallPeers` count as subdependencies.

Other resolution settings in `pnpm-workspace.yaml`:
- `autoDedupe` (v12.6.0, false): installs and adds pick one version satisfying every range in the workspace. Covers the whole workspace even with `--filter`. Frozen installs do not change the lockfile. Use `pnpm dedupe` otherwise; set it true if CI runs `pnpm dedupe --check`.
- `supportedArchitectures`: install optional dependencies for other platforms:

```yaml
supportedArchitectures:
  - linux-x64
  - linux-x64-musl
  - darwin-arm64
```
The list form (v12.5.0) accepts `<os>-<cpu>[-libc]` and Rust triples; the older `os`/`cpu`/`libc` map with `current` still works. It does not cross-compile addons.
- `optional: false` skips optional dependencies. `forceIgnoresPlatform` (v12.7.0): `--force` then also installs other-platform optionals.
- `update.ignoreDeps` lists packages to skip in `pnpm update` and `pnpm outdated`; patterns like `@babel/*` work. `allowedDeprecatedVersions` mutes deprecation warnings.

## Checked

2026-11-04. Confirmed resolutionMode semantics, registrySupportsTimeField and Verdaccio 5.15.1, autoDedupe (v12.6.0), supportedArchitectures including the v12.5.0 platform list, optional, forceIgnoresPlatform (v12.7.0), update.ignoreDeps and allowedDeprecatedVersions against pnpm.io/settings/other and /settings/dependency-resolution. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
