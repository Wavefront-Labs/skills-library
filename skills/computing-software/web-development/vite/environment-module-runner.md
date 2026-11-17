---
id: computing-software.web-development.vite.environment-module-runner
name: environment-module-runner
category: computing-software
field: web-development
product: vite
tags: [module-runner, module-evaluator, module-runner-transport, vite-module-runner-entry]
level: sme
status: docs-checked
description: "Create a ModuleRunner from vite/module-runner: options, ESModulesEvaluator, ModuleRunnerTransport (invoke or connect and send), worker thread and HTTP examples."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-runtimes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Import from `vite/module-runner` (a minimal entry). Unlike `server.ssrLoadModule`, the runner is decoupled from the server, so authors can supply their own transport.

```js
const moduleRunner = new ModuleRunner(
  { transport, createImportMeta: createNodeImportMeta },
  new ESModulesEvaluator(),
)
await moduleRunner.import('/src/entry-point.js')
```

Methods: `import(url)`, `clearCache()` (including HMR listeners), `close()` (does not stop the HMR connection), `isClosed()`. On a `full-reload` affected modules re-execute and `exports` is overridden, so call `import` again for fresh exports.

`ModuleRunnerOptions`: `transport`; `sourcemapInterceptor` (`false`, `'node'`, `'prepareStackTrace'` or an object); `hmr` (default `true`); `evaluatedModules` (custom cache).

`ModuleEvaluator`: `runInlinedModule(context, code, id)`, `runExternalModule(file)`, optional `startOffset`. `ESModulesEvaluator` uses `new AsyncFunction`, adding a 2-line offset; supply your own if the runtime forbids unsafe evaluation.

`ModuleRunnerTransport`: optional `connect(handlers)`, `disconnect`, `send`, `invoke(data)`, `timeout`. Without `invoke`, implement `send` and `connect`; Vite builds `invoke`. Pair it with a server `HotChannel`; emit `vite:client:connect` and `vite:client:disconnect`, keeping the client reference stable per connection. For an HTTP runner, use `hmr: false` and call `environment.hot.handleInvoke(payload)` on the server.

## Checked

2026-11-07. Confirmed against the `ModuleRunner`, `ModuleRunnerOptions`, `ModuleEvaluator` and `ModuleRunnerTransport` sections of guide/api-environment-runtimes.md (page read in full): the `vite/module-runner` entry, runner methods and the `close()` caveat, `full-reload` behaviour, option names and the `hmr` default, `ESModulesEvaluator` with `new AsyncFunction` and the 2-line offset, the `invoke` versus `send` plus `connect` rule, `vite:client:connect` and `vite:client:disconnect`, and the HTTP example with `hmr: false` and `handleInvoke`. Nothing removed.

Method: documentation only; no commands were run.
