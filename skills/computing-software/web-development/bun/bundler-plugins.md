---
id: computing-software.web-development.bun.bundler-plugins
name: bundler-plugins
category: computing-software
field: web-development
product: bun
tags: [bundler-plugins, on-resolve, on-load, virtual-modules]
level: advanced
status: docs-checked
description: "Write Bun bundler plugins with setup, onStart, onResolve, onLoad, onEnd and defer; build virtual modules and avoid namespace, filter and config gotchas."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/bundler/plugins.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```ts
import type { BunPlugin } from "bun";
const envPlugin: BunPlugin = {
  name: "virtual env",
  setup(build) {
    build.onResolve({ filter: /^env$/ }, () => ({ path: "env", namespace: "env" }));
    build.onLoad({ filter: /.*/, namespace: "env" }, () => ({
      contents: `export default ${JSON.stringify(process.env)}`,
      loader: "js",
    }));
  },
};
await Bun.build({ entrypoints: ["./app.ts"], outdir: "./out", plugins: [envPlugin] });
```

Hooks:
- `onStart(cb)`: bundler waits for all of them.
- `onResolve({filter, namespace?}, cb)`: cb gets `{path, importer}`, returns `{path, namespace?}`; return nothing for default resolution.
- `onLoad({filter, namespace?}, cb)`: cb gets `{path, namespace, loader, defer}`, returns `{contents?, loader?, exports?}`. Loader values: js, jsx, ts, tsx, json, jsonc, toml, yaml, file, napi, wasm, text, css, html.
- `onEnd(cb)`: gets `BuildOutput`; `Bun.build()` resolves after they finish.
- `onBeforeParse`: native (NAPI) hook, may run on any thread, so it must be thread-safe.

`filter` is a RegExp; `onResolve` runs it on the import string. Default namespace is `file`.

Gotchas:
- Hooks apply only when both filter and namespace match.
- Callbacks cannot change `build.config`; change it inside `setup()`.
- `defer()` waits for all other modules to load; call it at most once per onLoad.
- JS plugins run single-threaded.

## Checked

2026-11-04. Confirmed against the Bun docs page bundler/plugins: hook list and signatures, onStart awaited before continuing, onResolve returning path and namespace or nothing, onLoad arguments and return fields, the Loader union, onEnd and Bun.build() waiting for it, defer waiting for other modules and callable once per onLoad, config not modifiable from callbacks, default file namespace, JS plugins single-threaded, and onBeforeParse being a NAPI hook that must be thread-safe. Narrowed the filter note: the page says onResolve runs the filter on the import string and does not state the onLoad subject.
Method: documentation only; no commands were run.
