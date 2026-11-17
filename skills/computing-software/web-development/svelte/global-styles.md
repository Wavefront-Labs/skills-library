---
id: computing-software.web-development.svelte.global-styles
name: global-styles
category: computing-software
field: web-development
product: svelte
tags: [global-modifier, global-block, global-keyframes, unscoped-css, style-escape]
level: practitioner
status: docs-checked
description: "Escape Svelte style scoping with :global(...) for single selectors, :global { } blocks for groups, and -global- prefixed keyframe names."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/04-styling/02-global-styles.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`:global(...)` applies styles to a single selector globally:

```svelte
<style>
  :global(body) {
    /* applies to <body> */
    margin: 0;
  }

  div :global(strong) {
    /* all <strong> elements, in any component, inside <div> elements of this component */
    color: goldenrod;
  }

  p:global(.big.red) {
    /* <p> elements of this component with class="big red", even if applied programmatically */
  }
</style>
```

Global keyframes: prefix the name with `-global-`. The prefix is removed on compile, and elsewhere you reference it as `my-animation-name`.

```svelte
<style>
  @keyframes -global-my-animation-name { /* code goes here */ }
</style>
```

`:global { ... }` block for a group of selectors:

```svelte
<style>
  :global {
    /* every <div> in your application */
    div { ... }
    p { ... }
  }

  .a :global {
    /* every `.b .c .d` element, in any component, inside an `.a` element in this component */
    .b .c .d { ... }
  }
</style>
```

The `.a :global .b .c .d` form is equivalent (everything after `:global` is unscoped), though the nested form is preferred.

## Checked

Method: docs-only read of cited pages, 2026-11-08

Confirmed against the global styles page: :global(...), -global- keyframes, :global blocks and the equivalent `.a :global .b .c .d` form. Nothing removed.
