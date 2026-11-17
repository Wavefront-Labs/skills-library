---
id: computing-software.web-development.svelte.attach-tag
name: attach-tag
category: computing-software
field: web-development
product: svelte
tags: [attach-tag, attachments, attachment-factory, inline-attachment, conditional-attachment]
level: advanced
status: docs-checked
description: "Svelte attachments ({@attach}, 5.29+): functions run in an effect on mount and on state change, with cleanup, factories, inline forms and conditional use."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/09-%40attach.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Attachments are functions that run in an effect when an element is mounted, or when state read inside them updates. They may return a function called before the attachment re-runs and after the element is removed. Available in Svelte 5.29 and newer.

```svelte
<script>
  /** @type {import('svelte/attachments').Attachment} */
  function myAttachment(element) {
    console.log(element.nodeName); // 'DIV'
    return () => { console.log('cleaning up'); };
  }
</script>

<div {@attach myAttachment}>...</div>
```

An element can have any number of attachments.

Factories: a function can return an attachment, e.g. `{@attach tooltip(content)}`. Because `tooltip(content)` runs inside an effect, the attachment is destroyed and recreated whenever `content` (or state read inside) changes.

Inline: `<canvas {@attach (canvas) => {...}}>` works; nested `$effect`s inside rerun on their own state, while the outer function runs once if it reads no state.

Conditional: falsy values mean no attachment: `<div {@attach enabled && myAttachment}>`.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the {@attach} page: effect-based execution, cleanup return, Svelte 5.29+, factories re-created on state change, inline and conditional forms. Nothing removed.
