---
id: computing-software.web-development.svelte.props-updating
name: props-updating
category: computing-software
field: web-development
product: svelte
tags: [prop-mutation, ownership-invalid-mutation, callback-props, prop-reassignment, non-reactive-fallback]
level: practitioner
status: docs-checked
description: "Updating Svelte 5 props safely: temporary reassignment, why mutating plain-object props does nothing, the ownership_invalid_mutation warning, and callback props."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/02-runes/05-%24props.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
A prop reference updates when the parent's value changes. A child can temporarily override it by reassigning (`count += 1` on a destructured `count`), useful for unsaved ephemeral state.

Do not mutate props unless they are bindable (see `bindable-rune`):

- Plain object prop (`<Child object={{ count: 0 }} />`): `object.count += 1` has no effect.
- Reactive state proxy prop (`let object = $state({count: 0})` in the parent): the mutation does take effect, but you get an `ownership_invalid_mutation` warning because the child mutates state it does not own.
- Fallback value (`let { object = { count: 0 } } = $props()`): left untouched, not a state proxy, so mutations do not update the UI when the fallback is used. This applies to props not declared with `$bindable`.

Summary: do not mutate props. Communicate changes with callback props, or, if parent and child must share an object, use `$bindable`.

## Checked

2026-11-08. Read the $props page in full. Removed an unsupported troubleshooting line; the rest matched the Updating props section.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
