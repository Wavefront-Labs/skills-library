---
id: computing-software.web-development.vite.plugin-client-server-events
name: plugin-client-server-events
category: computing-software
field: web-development
product: vite
tags: [server-ws-send, client-to-server-events, custom-event-map, normalize-path, create-filter]
level: advanced
status: docs-checked
description: "Plugin and client messaging: server.ws.send, ws.on, hot.on and hot.send with prefixed event names, typing CustomEventMap, plus normalizePath and createFilter."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-plugin.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Server to client: `server.ws.send('my:greetings', { msg: 'hello' })`, for example inside `server.ws.on('connection', ...)`. Client: `import.meta.hot.on('my:greetings', (data) => ...)`. Always prefix event names to avoid collisions.

Client to server: `import.meta.hot.send('my:from-client', { msg: 'Hey!' })`; server:

```js
server.ws.on('my:from-client', (data, client) => {
  client.send('my:ack', { msg: 'Hi! I got your message!' })
})
```

Type payloads by extending `CustomEventMap` in a `.d.ts` file (include the `.d.ts` extension in the module path):

```ts
import 'vite/types/customEvent.d.ts'
declare module 'vite/types/customEvent.d.ts' {
  interface CustomEventMap { 'custom:foo': { msg: string } }
}
```

`InferCustomEventPayload<T>` uses it; unknown events are `any`.

Paths: Vite normalizes resolved ids to POSIX separators; compare using `normalizePath` exported from `vite`. For include/exclude use `createFilter` from `@rollup/pluginutils`, exposed by Vite.

## Checked

Date: 2026-11-07

Read api-plugin.md in full (Client-server Communication, Path Normalization, Filtering). Confirmed server.ws.send, hot.on, hot.send, server.ws.on with client.send, event prefix advice, CustomEventMap with the .d.ts path, InferCustomEventPayload, normalizePath from vite and createFilter. Nothing removed.

Method: documentation only; no commands were run.
