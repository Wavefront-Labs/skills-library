---
id: computing-software.web-development.vite.environment-api-concepts
name: environment-api-concepts
category: computing-software
field: web-development
product: vite
tags: [environment-api, environments-config, environment-inheritance, custom-environment-instances]
level: advanced
status: docs-checked
description: "Environment API concepts: client and ssr environments, the environments config option, inheritance and non-inherited options, EnvironmentOptions, release candidate status."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The Environment API is a release candidate: APIs stay stable between majors, though some specific ones are still experimental. Vite 6 formalized environments; before, there were an implicit `client` and optional `ssr`. A single dev server can now run code in several environments at once, sharing the HTTP server, middlewares, resolved config and plugin pipeline. The browser executes client code; other environments use a module runner.

An SPA or MPA needs no environment config: top-level options configure the `client` environment. For more, use `environments`:

```js
export default {
  build: { sourcemap: false },
  optimizeDeps: { include: ['lib'] },
  environments: { server: {}, edge: { resolve: { noExternal: true } } },
}
```

Environments inherit top-level options, except a few (such as `optimizeDeps`) marked non-inherited that apply only to `client`. Configure `client` via top-level options so its config does not change when you add environments.

`EnvironmentOptions`: `define`, `resolve`, `optimizeDeps`, `consumer` (`'client' | 'server'`), `dev`, `build`. In dev `client` and `ssr` always exist; in build `client` always, `ssr` only if configured (`environments.ssr` or `build.ssr`). The SSR environment may have another name.

Runtime providers supply instances, e.g. `environments: { ssr: customEnvironment({ build: { outDir: '/dist/ssr' } }) }`. The existing server API stays compatible; `server.moduleGraph` returns a mixed client/ssr view.

## Checked

2026-11-07. Confirmed against guide/api-environment.md, read in full: release-candidate notice, Vite 6 formalizing environments (implicit `client` and optional `ssr` before), the `environments` option and example, inheritance with `optimizeDeps` as the non-inherited example, the `EnvironmentOptions` fields, when `client` and `ssr` exist in dev and build (`environments.ssr` or `build.ssr`), the custom environment example, and the mixed `server.moduleGraph`. Nothing removed.

Method: documentation only; no commands were run.
