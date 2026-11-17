---
id: computing-software.web-development.vitepress.dynamic-routes-paths-loader
name: dynamic-routes-paths-loader
category: computing-software
field: web-development
product: vitepress
tags: [vitepress, dynamic-routes, paths-loader, params, paths-js, route-template, bracket-route]
level: advanced
status: docs-checked
description: "Generate many pages from one Markdown template with [param].md and a [param].paths.js loader that returns params objects."
sources:
  - https://raw.githubusercontent.com/vuejs/vitepress/main/docs/en/guide/routing.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A dynamic route lets one Markdown file produce many pages. The route parameter is written in the filename, e.g. `packages/[pkg].md`. Because VitePress is a static generator, possible paths must be known at build time, so the template **must** have a **paths loader file** next to it, named `[pkg].paths.js` (`.ts` also works):

```
packages/[pkg].md          # route template
packages/[pkg].paths.js    # route paths loader
```

The loader default-exports an object with a `paths` method returning an array of `{ params }` objects, one page each:

```js
export default {
  paths() {
    return [
      { params: { pkg: 'foo' } },
      { params: { pkg: 'bar' } }
    ]
  }
}
```

Output: `packages/foo.html` and `packages/bar.html`.

**Multiple params**: `[pkg]-[version].md` with params `{ pkg: 'foo', version: '1.0.0' }` produces `foo-1.0.0.html`.

**Dynamic paths.** The loader runs in Node at build time only, so it can read the filesystem or call APIs:

```js
import fs from 'node:fs'
export default {
  paths() {
    return fs.readdirSync('packages').map((pkg) => ({ params: { pkg } }))
  }
}
```

`paths` may be async (`await fetch(...)`) and may add `version` and other params.

Pitfalls: the template cannot be generated without the loader; params are serialized into the client payload, so keep them small (use the `content` property for bulk text, see the next skill).

## Checked

2026-11-04. Confirmed against the VitePress routing guide (Dynamic Routes, Paths Loader File, Multiple Params, Dynamically Generating Paths). Removed: the claim that param values must be URL-safe strings and the Verify step.

Method: documentation only; no commands were run.
