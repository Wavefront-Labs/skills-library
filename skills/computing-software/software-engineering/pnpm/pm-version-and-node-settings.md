---
id: computing-software.software-engineering.pnpm.pm-version-and-node-settings
name: pm-version-and-node-settings
category: computing-software
field: software-engineering
product: pnpm
tags: [pm-on-fail, engine-strict, node-version-setting, runtime-on-fail, tools-mirror, node-download-mirrors, recursive-install, loglevel, progress-setting]
level: practitioner
status: docs-checked
description: "Control how pnpm enforces its own version and Node.js: pmOnFail and removed-setting migration, engineStrict, nodeVersion, runtime, runtimeOnFail, tools mirrors, loglevel."
sources:
  - https://pnpm.io/settings/cli
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`pmOnFail` overrides `onFail` of `packageManager` and `devEngines.packageManager`:
- `download` (default): fetch and run the declared pnpm.
- `error`, `warn`, `ignore` (use when asdf, mise or Volta manage versions).
Set by `--pm-on-fail=ignore`, `pnpm_config_pm_on_fail=ignore`, or `pmOnFail: ignore`.

Removed settings map: `managePackageManagerVersions: true` is `download`, `false` is `ignore`, `packageManagerStrict: false` and `COREPACK_ENABLE_STRICT=0` are `warn`, `packageManagerStrictVersion: true` is `error`. `pnpm with` runs one command at a given version.

Node settings:
- `engineStrict` + `nodeVersion` (exact version, default `node -v`): reject dependencies incompatible with that Node, e.g. `nodeVersion: 12.22.0`. A project's own `engines` mismatch always fails. Optional dependencies are exempt; since v12.0.0 the exemption follows the edge, not the subtree.
- `runtime: false` skips `devEngines.runtime` and `engines.runtime` (read from workspace file, env or `--config.runtime`, not global config).
- `runtimeOnFail`: overrides runtime `onFail`; also governs Python interpreter downloads (v12.5.0) and the Rust toolchain (v12.11.0).
- `tools` (v12.5.0, global config or `PNPM_CONFIG_TOOLS` only): `node`, `bun`, `python`, `rust` with `mirror`; Node also `channels`.
- `nodeDownloadMirrors`: per-channel mirrors; machine-level since v12.4.0; mirror downloads carry registry credentials since v12.2.0.
- `npmPath`; `recursiveInstall` (true); `loglevel`; `progress` (v12.6.0); `color`; `reporter`.

## Checked

2026-11-04. Confirmed pmOnFail values and migration table, engineStrict and nodeVersion, runtime, runtimeOnFail, tools, nodeDownloadMirrors and the CLI settings with their version gates against pnpm.io/settings/cli. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
