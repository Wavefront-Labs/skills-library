---
id: computing-software.web-development.vite.environment-runtime-factories
name: environment-runtime-factories
category: computing-software
field: web-development
product: vite
tags: [environment-factory, hot-channel, skip-fs-check, create-server-hot-channel]
level: sme
status: docs-checked
description: "Runtime provider guide: environment factories returning EnvironmentOptions, building a DevEnvironment with a HotChannel transport, skipFsCheck and createServerHotChannel."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-runtimes.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
For runtime providers integrating an engine (Node.js, workerd, a Worker thread).

An environment factory returns `EnvironmentOptions` with defaults for the runtime, merged with user options via `mergeConfig`:

```ts
function createWorkerdEnvironment(userConfig: EnvironmentOptions): EnvironmentOptions {
  return mergeConfig({
    resolve: { conditions: [/*...*/] },
    dev: { createEnvironment(name, config) { return createWorkerdDevEnvironment(name, config, { hot: true, transport: customHotChannel() }) } },
    build: { createEnvironment(name, config) { return createWorkerdBuildEnvironment(name, config) } },
  }, userConfig)
}
```

Users then write `environments: { ssr: createWorkerdEnvironment({ build: { outDir: '/dist/ssr' } }) }`.

Defaults: `client` runs in the browser (module runner via `/@vite/client`); `ssr` runs in the Vite server's Node process. Build your own with `new DevEnvironment(name, config, { options, hot: true, transport })` where `transport` is a `HotChannel` (`on`, `send`).

`HotChannel` transports obey `server.fs` limits. If the channel is not exposed over the network (worker threads, in-process), set `skipFsCheck: true`.

Implement the most flexible communication level possible. For an SSR environment in the same Node process use the ready-made `createServerHotChannel()`:

```js
new DevEnvironment(name, config, { hot: true, transport: createServerHotChannel() })
```

## Checked

2026-11-07. Confirmed against guide/api-environment-runtimes.md, read in full: environment factories returning `EnvironmentOptions` with `mergeConfig`, the user config example, default `client` and `ssr` environments with `/@vite/client`, `new DevEnvironment` with a `HotChannel` (`on`, `send`), the `skipFsCheck: true` rule and `createServerHotChannel`. Nothing removed.

Method: documentation only; no commands were run.
