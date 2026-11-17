---
id: computing-software.web-development.elysia.set-elysia-constructor-options
name: set-elysia-constructor-options
category: computing-software
field: web-development
product: elysia
tags: [configuration, elysia-constructor, bun-serve, tls, body-size-limit, strict-path]
level: practitioner
status: docs-checked
description: "Set Elysia constructor options for prefix, normalize, strictPath, sanitize, and Bun serve settings such as TLS, body size limit and idle timeout."
sources:
  - https://elysiajs.com/patterns/configuration.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: change Elysia behaviour for one instance by passing a config object to `new Elysia({...})`.

## Common options

```ts
import { Elysia } from 'elysia'

new Elysia({
  prefix: '/v1',          // every route becomes /v1/...
  strictPath: true,       // /name matches, /name/ does not (default false tolerates both)
  normalize: true,        // default true
  sanitize: (value) => Bun.escapeHTML(value) // runs on every t.String during validation
})
```

- `normalize`: what to do with properties not in the schema on input or output. `true` (default) coerces to the schema using exact mirror; `'typebox'` uses TypeBox `Value.Clean`; `false` raises an error when a request or response has fields the schema does not allow.
- `name` and `seed` feed plugin deduplication. `seed.value` can be any type.
- `detail` and `tags` apply OpenAPI detail/tags to every route of the instance.
- `encodeSchema` (default `true`) runs custom `t.Transform` `Encode` before responding.
- `allowUnsafeValidationDetails` (since 1.4.13, default `false`) puts validation details in production error responses. Only enable on public APIs where leaking schema field names is acceptable.
- `nativeStaticResponse: true` (since 1.1.11) on Bun inlines static values into `Bun.serve.static`, e.g. `.get('/version', 1)`.
- `systemRouter`: on Bun uses `Bun.serve.routes`, falling back to Elysia's own router.
- `adapter` (since 1.1.11) picks a runtime adapter, e.g. `import { BunAdapter } from 'elysia/adapter/bun'`; the default is chosen from the environment.

## Server settings under `serve`

`serve` extends the Bun serve API and Bun TLS.

```ts
new Elysia({
  serve: {
    hostname: '0.0.0.0',                   // default 0.0.0.0
    port: 3000,                            // default 3000
    maxRequestBodySize: 1024 * 1024 * 256, // default 128MB
    idleTimeout: 60,                       // default 30 seconds
    tls: { cert: file('cert.pem'), key: file('key.pem') } // both required; import { file } from 'elysia'
  }
})
```

Other `serve` keys: `id` (hot reload id, `null` disables hot reload), `reusePort` (default true, forced on by Elysia), `unix` (socket instead of host+port), `rejectUnauthorized`, and `tls.ca`, `passphrase`, `requestCert` (default false), `lowMemoryMode`, `serverName`, `dhParamsFile`, `secureOptions`.

## WebSocket override

`websocket: { perMessageDeflate: true }` extends Bun's WebSocket config; the docs recommend leaving it at the default.

## Gotchas

- `aot: false` disables JIT entirely (the page says this gives faster startup time without cost of performance; the page lists `false` as the default under `aot`); `precompile: true` (since 1.0.0) compiles every route before the server starts, and the docs recommend leaving it `false`.
- Setting `strictPath` changes matching per RFC 3986; test trailing-slash clients.
- TLS needs both `cert` and `key`; a missing intermediate chain makes the handshake fail.

## Checked

2026-11-07. Read the whole Config page (patterns/configuration, from the elysiajs/documentation repo; the repo has no include or snippet files). Every option, default (`normalize` true, `strictPath` false, `encodeSchema` true, `allowUnsafeValidationDetails` false, `hostname` 0.0.0.0, `port` 3000, `maxRequestBodySize` 128MB, `idleTimeout` 30, `reusePort` true, `requestCert` false), "since" version and the `serve.tls` keys matched the page text. Corrected the `aot: false` note: the skill said "less speed" but the page says "without cost of performance".

Method: documentation only; no commands were run.
