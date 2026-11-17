---
id: computing-software.web-development.nuxt.nuxt-module-hooks-templates-types
name: nuxt-module-hooks-templates-types
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-module, add-template, add-type-template, nuxt-hooks]
level: sme
status: docs-checked
description: "Advanced module authoring: lifecycle hooks, custom hooks, virtual files via addTemplate, type templates and extending tsconfig contexts."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/4.modules/5.recipes-advanced.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Hooks: modules can hook into lifecycle hooks programmatically (`nuxt.hook('pages:extend', fn)`) or through the `hooks` map in their definition (for example `'app:error'`). If the module opens, handles or starts a watcher, close it in `nuxt.hook('close', async (nuxt) => {...})`.

Custom hooks: define and call your own hooks. If you expect other modules to subscribe, call them inside the `modules:done` hook, so every other module has had a chance to register listeners during its own `setup`. Declare a `ModuleHooks` interface for typing, then `await nuxt.callHook('my-module:custom-hook', payload)`.

Virtual files: `addTemplate({ filename: 'my-module-feature.mjs', dependsOn: [], getContents: () => 'export const myModuleFeature = () => "hello world !"' })` is importable from `#build/my-module-feature.mjs`. The `dependsOn: []` in the example skips regeneration when an existing file is edited in development; use it only when the output does not depend on watched file contents, otherwise declare named dependencies or a predicate to avoid stale output. For the server use `addServerTemplate` instead (importable in server code from the filename, for example `my-server-module.mjs`). To update templates, call `updateTemplates({ filter: t => t.filename === 'my-module-feature.mjs' })`, for example inside the `builder:watch` hook.

Type declarations: `addTypeTemplate({ filename: 'types/my-module.d.ts', getContents })` writes a template to disk and adds a reference to it in the generated `nuxt.d.ts`; the docs example augments `h3/rules` (`RouteRules`, `RouteRuleConfig`). For more granular control register a `prepare:types` hook callback and push `{ path: template.dst }` onto `references`.

Extend the TypeScript config: either push paths into `nuxt.options.typescript.tsConfig.include` (tsconfig.app.json), `sharedTsConfig` (tsconfig.shared.json), `nodeTsConfig` (tsconfig.node.json) or `serverTsConfig` (tsconfig.server.json), after `??= []`; or use `prepare:types` (`references`, `sharedReferences`, `nodeReferences`) and `nitro:prepare:types` (`references`). TypeScript references add files to the type context without being affected by `exclude` in tsconfig.json.

Augmenting types: Nuxt includes your module's directories in the right type contexts, so put the declaration file in the matching directory. `my-module/runtime/` is the app context (except `runtime/server`), `my-module/runtime/server/` the server context, and `my-module/` the node context (except `runtime/` and `runtime/server`).

Known limitation: server routes are also type-checked with tsconfig.app.json, in addition to tsconfig.server.json, because Nuxt infers server endpoint return types for `$fetch` and `useFetch`. Server-only types (for example for a virtual file from `addServerTemplate`, declared only in tsconfig.server.json) are then unknown to the app context and produce errors; declare such types in the app context as well.

## Checked

2026-11-04. Confirmed against the Nuxt "Use Hooks and Extend Types" page: hooks map and programmatic hooks, close hook, custom hooks and modules:done, addTemplate with dependsOn, addServerTemplate, updateTemplates, addTypeTemplate, prepare:types references, the four tsconfig options, the reference hooks, type contexts by directory, and the known limitation. Added the dependsOn staleness caveat and the custom-hook ModuleHooks interface from the page. Removed the Verify step.

Method: documentation only; no commands were run.
