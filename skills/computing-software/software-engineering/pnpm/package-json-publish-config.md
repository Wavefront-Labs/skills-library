---
id: computing-software.software-engineering.pnpm.package-json-publish-config
name: package-json-publish-config
category: computing-software
field: software-engineering
product: pnpm
tags: [publish-config-field, publish-config-registry, publish-config-directory, publish-config-name, executable-files, publish-field-override, scoped-registry-publish]
level: practitioner
status: docs-checked
description: "Use package.json publishConfig with pnpm: override main, exports and types at publish time, set registry, access, name, executableFiles and directory with linkDirectory."
sources:
  - https://pnpm.io/package_json
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`publishConfig` carries publish settings (kept in the published manifest) and overrides of manifest fields applied before packing.

```json
{
  "name": "foo",
  "main": "src/index.ts",
  "publishConfig": { "main": "lib/index.js", "typings": "lib/index.d.ts" }
}
```
publishes with `main: lib/index.js` and `typings: lib/index.d.ts`.

Overridable fields: `bin`, `main`, `exports`, `types`/`typings`, `module`, `browser`, `esnext`, `es2015`, `unpkg`, `umd:main`, `typesVersions`, `cpu`, `os`, `engines`, `name`.

Settings:
- `registry`: URL only; overrides the `registry` setting, scope routes and `--registry`. Auth is matched from `.npmrc`. In `pnpm publish -r` each package goes to its own registry; `--batch` sends one request per registry. `@<scope>:registry` (v12.7.0) wins for scoped packages.
- `access`: `public` or `restricted`, same as `--access`; unset sends nothing. Unscoped packages cannot be restricted.
- `name`: publish under another name when the manifest name is taken by a sibling (`foo-v2` published as `foo`). Dependents and the lockfile keep the manifest name.
- `executableFiles`: extra files that get +x; by default only `bin` entries do.
- `directory`: publish a subdirectory that must hold its own `package.json`. `linkDirectory` (default true) symlinks the project from that directory in local development.

## Checked

2026-11-04. Confirmed the overridable field list, registry, @<scope>:registry (v12.7.0), access, name, executableFiles, directory and linkDirectory against pnpm.io/package_json. Removed the unsourced closing Check line.

Method: documentation only; no commands were run.
