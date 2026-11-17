---
id: computing-software.web-development.svelte.bind-input-basics
name: bind-input-basics
category: computing-software
field: web-development
product: svelte
tags: [bind-directive, bind-value, bind-checked, bind-group, function-bindings]
level: intro
status: docs-checked
description: "Svelte bind: on inputs: syntax and shorthand, function bindings (5.9+), numeric coercion, form reset defaults, checked, indeterminate and bind:group for radios and checkboxes."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/12-bind.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`bind:property={expression}` lets data flow from child to parent. The expression must be an lvalue (variable or object property). `bind:value` is shorthand for `bind:value={value}`. If the element already listens for the same event, that listener fires before the bound value updates. Most bindings are two-way; a few are readonly.

Function bindings (Svelte 5.9.0+): `bind:value={() => value, (v) => value = v.toLowerCase()}` validates or transforms. For readonly bindings the getter is `null`: `bind:clientWidth={null, redraw}`.

`bind:value` on `<input>`: for `type="number"` or `"range"` the value is coerced to a number; if empty or invalid it is `undefined`. Since 5.6.0, an input with `defaultValue` in a form reverts to that on reset (initial render still uses the binding unless `null` or `undefined`).

`bind:checked` for checkboxes; since 5.6.0 `defaultChecked` works the same way. Use `bind:group` for radios, not `bind:checked`.

`bind:indeterminate` binds the indeterminate state independently of checked.

`bind:group`: grouped radios are mutually exclusive and bind one value; grouped checkboxes populate an array.

```svelte
<input type="radio" bind:group={tortilla} value="Plain" />
<input type="checkbox" bind:group={fillings} value="Rice" />
```

`bind:group` only works if the inputs are in the same Svelte component.

## Checked

2026-11-08: Read the bind page sections on syntax, function bindings (5.9.0), input value, checked, indeterminate and group (5.6.0 defaultValue and defaultChecked). Every claim was located; nothing removed.

Method: docs-only read of cited pages, 2026-11-08
