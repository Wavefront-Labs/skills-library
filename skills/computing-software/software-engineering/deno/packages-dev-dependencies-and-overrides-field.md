---
id: computing-software.software-engineering.deno.packages-dev-dependencies-and-overrides-field
name: packages-dev-dependencies-and-overrides-field
category: computing-software
field: software-engineering
product: deno
tags: [packages, dev-dependencies, install-prod, entrypoint, overrides, package-json, jsr-in-package-json]
level: practitioner
status: docs-checked
description: "Handle dev-only dependencies without a devImports field, install production-only sets, use JSR in package.json, and pin transitive versions with overrides."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Deno loads and installs only dependencies actually used by executed code, so it has no `devImports` field. Marking dev dependencies is a convention: add a `// dev` comment in deno.json, or use `devDependencies` in package.json.

```json title="deno.json"
{
  "imports": {
    "@std/fs": "jsr:@std/fs@1",
    "@std/testing": "jsr:@std/testing@1" // dev
  }
}
```

Production-only installs:

- `deno install --prod` skips `devDependencies`; add `--skip-types` to also exclude `@types/*`.
- `deno install --entrypoint` installs only what the entrypoint transitively imports; with `--prod`, type-only dependencies are also excluded.

JSR packages can be depended on from `package.json` using the `jsr:` scheme, installed with `deno install`:

```json title="package.json"
{
  "dependencies": {
    "@std/path": "jsr:^1.0.9"
  }
}
```

`overrides` in `package.json` controls transitive versions:

```json title="package.json"
{
  "dependencies": { "express": "^4.18.0" },
  "overrides": {
    "cookie": "0.7.0",
    "express": { "qs": "6.13.0" }
  }
}
```

Here `cookie` is pinned globally while `qs` is overridden only where `express` requires it.

Set `"preferPackageJson": true` in deno.json to make `deno add`/`install`/`remove` write to package.json.

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: dev dependency convention, `--prod`, `--skip-types`, `--entrypoint`, `jsr:` in package.json, `overrides` example, `preferPackageJson`. Nothing removed.

Method: documentation only; no commands were run.
