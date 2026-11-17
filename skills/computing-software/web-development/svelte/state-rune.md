---
id: computing-software.web-development.svelte.state-rune
name: state-rune
category: computing-software
field: web-development
product: svelte
tags: [state-rune, reactive-state, deep-reactivity, state-proxy, state-class-fields]
level: intro
status: docs-checked
description: "Declare reactive state with the $state rune: plain variables, deeply reactive proxies for arrays and simple objects, destructuring pitfalls, and $state in class fields."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/02-%24state.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`let count = $state(0);` makes `count` reactive; it is just a number, updated like any variable (`count++`).

Deep state: with an array or simple object, `$state` returns a deeply reactive proxy, so `todos[0].done = !todos[0].done` and `todos.push({...})` trigger granular updates. Pushed objects are proxified too. Proxying stops at anything that is not an array or simple object (a class instance, `Object.create`). Updating a proxy does not mutate the original object.

Destructuring (`let { done } = todos[0]`) evaluates once, so the result is not reactive.

Classes: instances are not proxied. Use `$state` in class fields (public or private) or as the first assignment to a property in the `constructor`:

```js
class Todo {
  done = $state(false);
  constructor(text) { this.text = $state(text); }
  reset = () => { this.text = ''; this.done = false; }
}
```

The compiler turns the fields into `get`/`set` on the prototype, so they are not enumerable. Pass `onclick={todo.reset}` only if `reset` is an arrow function; otherwise use `onclick={() => todo.reset()}`, because `this` would be the button.

Reactive `Set`, `Map`, `Date` and `URL` come from `svelte/reactivity`.

## Checked

2026-11-08: Read the $state page (deep proxies, destructuring, classes, get/set on prototype, this and arrow functions, svelte/reactivity classes). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
