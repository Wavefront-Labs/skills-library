---
id: computing-software.web-development.vite.environment-plugins-hooks
name: environment-plugins-hooks
category: computing-software
field: web-development
product: vite
tags: [this-environment, config-environment-hook, hot-update-hook, apply-to-environment]
level: advanced
status: docs-checked
description: "Environment-aware plugins: global vs per-environment hooks, this.environment, registering environments in config, configEnvironment, hotUpdate and applyToEnvironment."
sources:
  - https://raw.githubusercontent.com/vitejs/vite/main/docs/guide/api-environment-plugins.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Global hooks run once (config resolution, server hooks); per-environment hooks run per environment and expose `this.environment` (all Rolldown hooks and module-handling Vite hooks). `buildStart` and `buildEnd` run only for `client` in dev unless the plugin sets `perEnvironmentStartEndDuringDev: true`; likewise `perEnvironmentWatchChangeDuringDev` for `watchChange`.

Use `this.environment.config` to vary processing, e.g. `this.environment.config.resolve.conditions`. Register an environment in `config` (an empty object is enough):

```ts
config: () => ({ environments: { rsc: { resolve: { conditions: ['react-server', ...defaultServerConditions] } } } })
```

`configEnvironment(name, options, env)`: per environment, after defaults are resolved; return partial options:

```ts
configEnvironment(name) { if (name === 'rsc') return { resolve: { conditions: ['workerd'] } } }
```

`hotUpdate` replaces `handleHotUpdate` per environment. Options: `type` (`create`/`update`/`delete`), `file`, `timestamp`, `modules`, `read`, `server`. Run once per environment in `server.environments` order; send with `this.environment.hot.send({ type: 'full-reload' })` and return `[]`.

State shared across environments must key on `this.environment` (a `Map<Environment, State>`).

`applyToEnvironment(environment)` returns `true`, `false` or a replacement plugin. `perEnvironmentPlugin(name, (environment) => plugin)` is a helper; the returned plugin must not use Vite-specific hooks. It runs after `configResolved`.

## Checked

2026-11-07. Confirmed against guide/api-environment-plugins.md, read in full: global versus per-environment hooks, `buildStart`/`buildEnd` with `perEnvironmentStartEndDuringDev` and `watchChange` with `perEnvironmentWatchChangeDuringDev`, registering environments in `config`, `configEnvironment`, the `hotUpdate` options and full-reload example, `Map<Environment, State>` keying, `applyToEnvironment`, `perEnvironmentPlugin`, and that it runs after `configResolved`. Nothing removed.

Method: documentation only; no commands were run.
