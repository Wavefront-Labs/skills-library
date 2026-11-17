---
id: computing-software.web-development.nuxt.nuxt-module-best-practices
name: nuxt-module-best-practices
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-module, best-practices, async-setup, prefix-exports]
level: advanced
status: docs-checked
description: "Module authoring rules: avoid slow async setup (warning beyond 1 second) and prefix every exposed component, composable, route and config."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/4.modules/7.best-practices.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Async setup: modules can be asynchronous, but Nuxt waits for your module to set up before going to the next module and starting the dev server, build process and so on. Prefer deferring time-consuming logic to Nuxt hooks. If a module takes more than 1 second to set up, Nuxt emits a warning.

Prefix your exports: give an explicit prefix to any exposed configuration, plugin, API, composable, component or server route, to avoid conflicts with other modules, Nuxt internals or user code. Ideally use the module name. For a module called `nuxt-foo`:

| Type | Avoid | Prefer |
|---|---|---|
| Components | `<Button>`, `<Modal>` | `<FooButton>`, `<FooModal>` |
| Composables | `useData()`, `useModal()` | `useFooData()`, `useFooModal()` |
| Server routes | `/api/track`, `/api/data` | `/api/_foo/track`, `/api/_foo/data` |

Server routes matter most, because paths like `/api/auth`, `/api/login` or `/api/user` are very likely already used by the application. Use a unique prefix: `/api/_foo/...` (underscore prefix) or `/_foo/...` for non-API routes.

Lifecycle hooks: for one-time setup (generating config files, setting up databases, installing dependencies) use `onInstall (nuxt)` and `onUpgrade (nuxt, options, previousVersion)` on the module definition instead of running that logic in `setup`, which runs on every build. The docs example gives `meta` a `name` and `version` and checks `previousVersion` in `onUpgrade` for version-specific migrations.

Other guidelines from the page:
- Be TypeScript friendly: exposing types and developing in TypeScript benefits users even when they do not use TypeScript.
- Use ESM syntax: Nuxt relies on native ESM.
- Document the module in the readme: why use it, how to use it, what it does; link to the integration website and documentation.
- Provide a demo: a minimal reproduction with StackBlitz linked from the readme.
- Stay version agnostic: say "X for Nuxt", not "X for Nuxt 3", and prefer `meta.compatibility` for Nuxt version constraints.
- Follow the module starter conventions (for example its ESLint configuration) so the code style matches other community modules.

## Checked

2026-11-04. Confirmed against the Nuxt "Follow Best Practices" page: async setup behaviour and the 1 second warning, prefix table and server route prefixes, onInstall/onUpgrade lifecycle hooks, and each of the remaining guidelines. Removed the draft's "related rules" sentence (meta.name/configKey, secrets, runtime/app, close hook), which comes from other pages, not this one, and the Verify step. Added the lifecycle-hook and guideline items the draft omitted.

Method: documentation only; no commands were run.
