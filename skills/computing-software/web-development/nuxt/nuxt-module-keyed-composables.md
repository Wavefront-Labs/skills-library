---
id: computing-software.web-development.nuxt.nuxt-module-keyed-composables
name: nuxt-module-keyed-composables
category: computing-software
field: web-development
product: nuxt
tags: [nuxt, nuxt-module, keyed-composables, optimization, compiler]
level: sme
status: docs-checked
description: "Register module functions as keyed composables so Nuxt injects a unique hash key, with argumentLength rules and static-analysis limits."
sources:
  - https://github.com/nuxt/nuxt/blob/main/docs/3.guide/4.modules/3.recipes-basics.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Functions such as `useState` and `useAsyncData` need state consistency between server and client. A module can register its own functions for automatic key injection: when a registered function is called with fewer than the specified number of arguments, Nuxt's compiler injects a unique key as an additional argument. The key is a hash derived from the file path and call location, and stays stable between server-side rendering and client hydration.

```ts
nuxt.options.optimization.keyedComposables.push({
  name: 'useMyState',
  source: resolver.resolve('./runtime/composables/state'),
  argumentLength: 2,
})
```

Properties:
- `name` (`string`): the function name. Use `'default'` for default exports; the callable name is then derived from the filename in camelCase.
- `source` (`string`): resolved path to the file where the function is defined; supports Nuxt aliases (`~`, `@`, etc.).
- `argumentLength` (`number`): maximum number of arguments the function accepts. When called with fewer, a unique key is injected.

With `argumentLength: 2`: `useMyState()` becomes `useMyState('$HJiaryoL2y')`, `useMyState('myKey')` becomes `useMyState('myKey', '$HJiaryoL2y')`, and `useMyState('a', 'b')` is not transformed because it already has 2 arguments.

Limits from the docs:
- The key injection plugin verifies the exact resolved import source of each call and does not follow barrel exports. The function must be exported from the exact file in `source`: importing from `my-module/runtime/composables/state` works, importing from `my-module/runtime/composables` (an index.ts barrel) does not.
- Calls must be statically analyzable. Direct calls and calls on a namespace import (`composables.useMyState()`) work. Dynamic property access (`composables[name]()`), reassigning to a variable (`const myFn = useMyState; myFn()`), passing as a callback (`someFunction(useMyState)`) and destructuring with renaming in a nested scope (`const { useMyState: localState } = composables`) do not.

## Checked

2026-11-04. Confirmed against the Nuxt "Add Plugins, Components and More" page, section "Add Keyed Functions": behaviour, hash note, the keyedComposables push, the property table, the argumentLength example, and both warnings. Added the destructuring-with-renaming failure case the page lists. Removed the draft's advice to make the key the last parameter and to treat injection as a build-time convenience (not on the page) and the Verify step.

Method: documentation only; no commands were run.
