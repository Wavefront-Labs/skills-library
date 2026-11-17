---
id: computing-software.web-development.svelte.bindable-rune
name: bindable-rune
category: computing-software
field: web-development
product: svelte
tags: [bindable-rune, two-way-binding, bind-component-prop, bindable-fallback, child-to-parent-data]
level: practitioner
status: docs-checked
description: "Mark Svelte props as bindable with $bindable so data flows up via bind:, including fallback values and the non-undefined rule when the parent binds."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/06-%24bindable.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Props normally flow one way, parent to child. Bound props let data flow up and let a state proxy be mutated in the child. Use sparingly: overuse makes data flow unpredictable.

Child:

```svelte
<script>
  let { value = $bindable(), ...props } = $props();
</script>
<input bind:value={value} {...props} />
```

Parent:

```svelte
<script>
  import FancyInput from './FancyInput.svelte';
  let message = $state('hello');
</script>
<FancyInput bind:value={message} />
<p>{message}</p>
```

The parent does not have to use `bind:`; it may pass a normal prop. Provide a fallback for when nothing is passed:

```js
let { value = $bindable('fallback'), ...props } = $props();
```

When a bindable prop has a fallback and the parent uses `bind:`, the parent must pass a value other than `undefined`, to avoid ambiguity about which value applies.

Mutating non-bindable props is strongly discouraged; Svelte warns if a component mutates state it does not own.

## Checked

2026-11-08. Read the $bindable page in full. Removed an unsupported claim that a runtime error is thrown when the parent binds undefined (the page states only the rule); the rest matched.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
