---
id: computing-software.web-development.vite.environment-plugin-communication-build
name: environment-plugin-communication-build
category: computing-software
field: web-development
product: vite
tags: [environment-hot-channel, client-connect-event, shared-during-build, shared-config-build]
level: advanced
status: docs-checked
description: "environment.hot messaging with per-connection clients (vite:client:connect), and building all environments in one process: sharedDuringBuild and builder.sharedConfigBuild."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`environment.hot` is client-server communication for any environment that supports HMR. Several application instances may share an environment (each browser tab is one). On connect Vite emits `vite:client:connect` on that `hot` instance, and `vite:client:disconnect` on close. Handlers get a `NormalizedHotChannelClient` as the second argument; its `send` targets that one instance, and the reference is stable per connection.

```js
configureServer(server) {
  server.environments.ssr.hot.on('my:greetings', (data, client) => {
    client.send('my:foo:reply', `Hello from server! You said: ${data}`)
  })
  server.environments.ssr.hot.send('my:foo', 'Hello from server!') // broadcast
}
```

The app side uses `import.meta.hot` as usual.

In build hooks (`renderChunk`, `generateBundle` and others) plugins also get the environment instead of an `ssr` boolean.

Shared plugins during build: Vite 6 builds all environments in one process. For backward compatibility each environment gets its own `ResolvedConfig` by default, because plugins use `config.build` rather than `environment.config.build`. A project opts into a shared config and pipeline with `builder.sharedConfigBuild: true`. A plugin author opts a single plugin into one shared instance with `sharedDuringBuild: true`.

## Checked

2026-11-04. Confirmed against the Vite Environment API for Plugins guide (docs/guide/api-environment-plugins.md): environment.hot messaging, vite:client:connect and disconnect events, NormalizedHotChannelClient, build-hook environment, builder.sharedConfigBuild and sharedDuringBuild. Nothing removed.

Method: documentation only; no commands were run.
