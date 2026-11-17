---
id: computing-software.software-engineering.deno.packages-vendoring-and-overrides
name: packages-vendoring-and-overrides
category: computing-software
field: software-engineering
product: deno
tags: [packages, vendor, links, scopes, override, local-npm, offline]
level: advanced
status: docs-checked
description: "Vendor remote modules, override dependencies with links (JSR and npm) and replace HTTPS imports with patched local files via scopes."
sources:
  - https://raw.githubusercontent.com/denoland/docs/main/runtime/packages/index.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Vendoring stores remote dependencies locally (useful on CI, in Docker, or to patch them):

```json
{ "vendor": true }
```

Deno then caches dependencies into a `vendor` directory when the project runs, or immediately with `deno install --entrypoint main.ts`. Afterwards `deno run --cached-only main.ts` works offline.

`links` overrides JSR and npm packages with local directories (like `npm link`):

```json title="deno.json"
{ "links": ["../some-package-or-workspace"] }
```

Referencing one package inside a workspace includes the whole workspace. Only respected in the workspace root; elsewhere it warns. Git-based overrides are unavailable.

Local npm packages need a `node_modules` directory. With `"nodeModulesDir": "auto"` it is recreated each run; with `"manual"` (default alongside package.json) run `deno install` after changes. Overriding purges npm packages from the lockfile, and the package name must still exist in the registry.

Override HTTPS imports with `scopes` (root only; nested scopes in dependencies are ignored):

```json title="deno.json"
{
  "imports": {
    "example/": "https://deno.land/x/example/"
  },
  "scopes": {
    "https://deno.land/x/example/": {
      "https://deno.land/x/my-library@1.0.0/mod.ts": "./patched/mod.ts"
    }
  }
}
```

## Checked

2026-11-04. Confirmed against the Deno Dependency management page: `vendor: true` and `deno install --entrypoint`, `links` rules and limitations, local npm package behaviour by `nodeModulesDir`, `scopes` override. The deno.land/x URLs are illustrative import strings in the example, not pages cited as sources. Nothing removed.

Method: documentation only; no commands were run.
