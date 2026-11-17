---
id: computing-software.web-development.svelte.inspect-rune
name: inspect-rune
category: computing-software
field: web-development
product: svelte
tags: [inspect-rune, inspect-trace, reactive-debugging, dev-only, console-log-alternative]
level: practitioner
status: docs-checked
description: "Debug Svelte reactivity with $inspect, $inspect(...).with for custom callbacks, and $inspect.trace (5.14+) to find which state triggered an effect."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/07-%24inspect.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`$inspect` works only in development; in a production build it is a no-op. It is like `console.log` but re-runs when its argument changes, tracking state deeply (updates inside objects and arrays re-fire). On updates it prints a stack trace to find the origin of the change (not in the playground).

```svelte
$inspect(count, message); // logs when either changes
```

`$inspect(...).with(callback)`: the callback is invoked instead of `console.log`. Its first argument is `"init"` or `"update"`, followed by the inspected values.

```js
$inspect(count).with((type, count) => {
  if (type === 'update') {
    debugger; // or console.trace
  }
});
```

`$inspect.trace(label?)`, added in 5.14: traces the surrounding function in development. Whenever it re-runs as part of an effect or derived, the console shows which reactive state caused it. It must be the first statement of a function body.

```js
$effect(() => {
  $inspect.trace();
  doSomeWork();
});
```

## Checked

2026-11-08. Read the $inspect page in full. All claims matched; no claims changed.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
