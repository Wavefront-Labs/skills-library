---
id: computing-software.software-engineering.pnpm.package-json-engines-and-runtime
name: package-json-engines-and-runtime
category: computing-software
field: software-engineering
product: pnpm
tags: [package-manager-field, dev-engines-package-manager, engines-field, engines-runtime-field, dev-engines-runtime-field, pm-on-fail, runtime-on-fail, package-json5-yaml]
level: practitioner
status: docs-checked
description: "Pin tooling in package.json for pnpm: engines, engines.runtime, devEngines.runtime, packageManager versus devEngines.packageManager ranges, onFail and json5/yaml manifests."
sources:
  - https://pnpm.io/package_json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```json
{
  "packageManager": "pnpm@12.0.0",
  "devEngines": {
    "runtime": { "name": "node", "version": "^24.4.0", "onFail": "download" },
    "packageManager": { "name": "pnpm", "version": ">=12.0.0 <13.0.0", "onFail": "download" }
  },
  "engines": { "node": ">=10", "pnpm": ">=3" }
}
```

- `engines`: local development fails if pnpm's version does not match; for installed dependencies it only warns unless `engineStrict` is set.
- `engines.runtime`: a dependency declares the Node.js it needs; pnpm installs it, binds CLI apps to it and runs `postinstall` with it.
- `devEngines.runtime`: one object or an array of node, deno, bun. `pnpm install` resolves the range, saves exact version and checksum in the lockfile, and scripts use that runtime. `runtimeOnFail` overrides `onFail`. Since v12.0.0-rc.2 a bare `node` inside the project follows the pin; disable with `globalShims` or bypass with `PNPM_SHIM_BYPASS=1`.
- `packageManager`: exact version; a different running pnpm switches to it as set by `pmOnFail`. When pnpm 12 is declared this way and `pmOnFail` is not `ignore`, resolution info goes into a leading boot document in `pnpm-lock.yaml`.
- `devEngines.packageManager`: supports ranges; resolved version stored under `packageManagerDependencies`. With no recorded version pnpm records the running one if it satisfies the range and passes `minimumReleaseAge`, else the newest old-enough version. Can name `npm`, `yarn` or `bun` (v12.0.0-rc.6), pinned outside the lockfile.
- pnpm also reads `package.json5` and `package.yaml`.

## Checked

2026-11-04. Confirmed engines, engines.runtime, devEngines.runtime, packageManager, devEngines.packageManager, the boot-document note, version gates and json5/yaml support against pnpm.io/package_json. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
