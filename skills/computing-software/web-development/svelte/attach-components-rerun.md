---
id: computing-software.web-development.svelte.attach-components-rerun
name: attach-components-rerun
category: computing-software
field: web-development
product: svelte
tags: [attachment-symbol-key, wrapper-components, create-attachment-key, from-action, attachment-rerun]
level: advanced
status: docs-checked
description: "Svelte attachments on components and spreads: Symbol-keyed props, wrapper components, controlling re-runs with getter functions, createAttachmentKey and fromAction."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/09-%40attach.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
On a component, `{@attach ...}` creates a prop whose key is a `Symbol`. If the component spreads its props onto an element, that element receives the attachments, which lets you write wrapper components:

```svelte
<!-- Button.svelte -->
<script>
  /** @type {import('svelte/elements').HTMLButtonAttributes} */
  let { children, ...props } = $props();
</script>

<!-- `props` includes attachments -->
<button {...props}>{@render children?.()}</button>
```

Use as `<Button {@attach tooltip(content)}>Hover me</Button>`.

Re-running: unlike actions, attachments are fully reactive. `{@attach foo(bar)}` re-runs on changes to `foo`, `bar` or any state read inside `foo`. If that is a problem (expensive unavoidable setup), pass a getter and read it in a child effect:

```js
function foo(getBar) {
  return (node) => {
    veryExpensiveSetupWork(node);
    $effect(() => { update(node, getBar()); });
  };
}
```

Helpers from `svelte/attachments`:
- `createAttachmentKey` adds attachments to an object that will be spread onto an element or component.
- `fromAction` converts an action-only library's action into an attachment, e.g. to use it with components.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the Svelte `{@attach ...}` docs page: Symbol-keyed props on components, the Button wrapper example, re-run behaviour and the getter-plus-child-effect pattern, `createAttachmentKey` and `fromAction`. Nothing removed.
