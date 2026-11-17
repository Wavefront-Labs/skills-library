---
id: computing-software.web-development.svelte.style-directive
name: style-directive
category: computing-software
field: web-development
product: svelte
tags: [style-directive, inline-styles, important-modifier, css-custom-property-inline, style-precedence]
level: intro
status: docs-checked
description: "Set inline styles in Svelte with style:property: expressions, shorthand, |important, precedence over style attributes (even !important), and custom properties."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/17-style.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`style:` is shorthand for setting multiple styles on an element.

```svelte
<!-- These are equivalent -->
<div style:color="red">...</div>
<div style="color: red;">...</div>
```

Values can be expressions: `style:color={myColor}`. Shorthand when the variable has the property name: `style:color`. Combine several:

```svelte
<div style:color style:width="12rem" style:background-color={darkMode ? 'black' : 'white'}>...</div>
```

Mark as important with `|important`:

```svelte
<div style:color|important="red">...</div>
```

Precedence: when `style:` directives are combined with a `style` attribute, the directives win, even over `!important` properties:

```svelte
<div style:color="red" style="color: blue">This will be red</div>
<div style:color="red" style="color: blue !important">This will still be red</div>
```

Custom properties work too: `<div style:--columns={columns}>...</div>`.

## Checked

Method: docs-only read of cited pages, 2026-11-08
