---
id: computing-software.devops-ci-cd.nx.nx-ready-signal
name: nx-ready-signal
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, monorepo, readywhen, signal, emitreadysignal, nx-ready-url, dev-server]
level: sme
status: docs-checked
description: "Report Nx server readiness from inside the task: readyWhen signal, supported plugins, NX_READY_URL, getReadyUrl and emitReadySignal usage."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/project-configuration.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: let a server tell Nx exactly when and where it listens, instead of Nx probing from outside.

```json
"serve": { "continuous": true, "readyWhen": { "signal": true } }
```
Plugins and executors that report once listening: `NxAppWebpackPlugin`, `NxAppRspackPlugin`, `NxReadySignalPlugin`, the `nxReadySignal()` Vite plugin, `pluginNxReadySignal()` for Rsbuild, the `@nx/nuxt/ready-signal` module, `@nx/web:file-server`, `@nx/js:verdaccio`, and any executor/builder returning success with a `baseUrl` (e.g. `@angular/build:dev-server`; `0.0.0.0` or `[::]` reported as `localhost`). The report carries the actual port, however chosen.

Inferred checks use `command` instead for Angular (`@nx/angular/plugin`), Next.js (`next dev`/`next start`), Expo, Nuxt (when the module is not loaded), React Router serve, and Storybook (waits only if a port is set via `--port`, `SBCONFIG_PORT`, or `PORT`). Webpack/Rspack/Vite/Rsbuild infer `signal` only when the config loads the plugin.

Consuming the address: a waiting task gets `NX_READY_URL` when exactly one awaited target reported one (even a server started in another terminal). `getReadyUrl('http://localhost:4200/app')` from `@nx/devkit` takes protocol and port from it, keeps the path/query, and returns the input unchanged if unset.

Custom server: call `emitReadySignal(server)` (or a URL string) from `@nx/js/ready-signal` once listening; guard with `if (process.env.NX_READY_SIGNAL_SOCKET)` and load it dynamically (the doc uses `new Function('s', 'return import(s)')` so bundlers leave it alone and a missing `@nx/js` is caught). Code already depending on `@nx/devkit` can import it from there. It does nothing outside a `signal` task.

Gotchas: a `signal` check passes only on the report. If you change an inferred dev command to one that does not report, set `readyWhen` yourself or waiting tasks time out. WASM Nx can run `signal` and port-0 checks but not other checks.

To inspect: `nx show target` shows a target's `readyWhen` with the timeout and where the check came from; the project details in `nx graph` show the check and its source.

## Checked

2026-11-07. Confirmed: readyWhen signal, plugin list, inferred command checks, NX_READY_URL, getReadyUrl and emitReadySignal against Project configuration. Removed: an invented Verify step (replaced by the page's nx show target / nx graph statement).

Method: documentation only; no commands were run.
