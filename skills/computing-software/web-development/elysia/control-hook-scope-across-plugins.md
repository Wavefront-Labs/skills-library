---
id: computing-software.web-development.elysia.control-hook-scope-across-plugins
name: control-hook-scope-across-plugins
category: computing-software
field: web-development
product: elysia
tags: [elysia, plugin, key-concept, scope, encapsulation, as-global]
level: advanced
status: docs-checked
description: "Decide whether an Elysia hook stays local, is scoped to the parent, or goes global, using inline as, guard as or instance as, and lift scope up one level."
sources:
  - https://elysiajs.com/essential/plugin.html
  - https://elysiajs.com/key-concept.html
  - https://elysiajs.com/essential/life-cycle.html
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Goal: make a plugin's hook or derived value reach (or not reach) the instances that use it.

## Encapsulation

Lifecycle hooks are isolated to the instance that declares them, like unexported module members. A plugin's `state` and `decorate` are inherited by the parent, but its lifecycle is not:

```typescript
const profile = new Elysia()
	.onBeforeHandle(({ cookie }) => throwIfNotSignIn(cookie))
	.get('/profile', () => 'Hi there!')

new Elysia().use(profile).patch('/rename', ...)   // NOT sign-in checked
```

## Three scope levels

| as | child | current | parent | main |
| --- | --- | --- | --- | --- |
| local (default) | yes | yes | no | no |
| scoped | yes | yes | yes | no |
| global | yes | yes | yes | yes |

Scoped reaches one parent only.

## Three ways to set scope

1. Inline, per hook: `.onBeforeHandle({ as: 'global' }, fn)` or `.derive({ as: 'scoped' }, fn)`.
2. Guard, for all hooks and schema inside: `.guard({ as: 'scoped', response: t.String(), beforeHandle() {...} })`. Guard-as does not support `derive` and `resolve`.
3. Instance, for everything declared so far: `new Elysia().derive(...).get(...).as('scoped')`.

## Lifting further

`as('scoped')` on an instance lifts its local hooks and schema up one level. To reach a grandparent, call `.as('scoped')` again in the intermediate instance. In the docs' example the lifted `response: t.String()` makes `.get('/ok', () => 3)` in the parent a type error.

## Which to pick

Global dependencies fit plugins that add no types (cors, compress, helmet) or global lifecycle (tracing, logging). Plugins that add types or business logic (macro, state, model, Auth, Database) should be explicit dependencies applied with `.use()` where needed.

## Gotchas

- `onRequest` is always global.
- Hooks are inherited only by routes registered after them.

## Checked

Checked 2026-11-07 against the Elysia documentation source (essential/plugin.html, key-concept.html, essential/life-cycle.html); each claim, option name and default was compared with the page text. Added the life-cycle page as a source for the onRequest-is-global claim.

Method: documentation only; no commands were run.
