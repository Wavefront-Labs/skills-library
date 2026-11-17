---
id: computing-software.web-development.svelte.html-tag
name: html-tag
category: computing-software
field: web-development
product: svelte
tags: [html-tag, at-html, raw-html, xss-prevention, global-styles-for-html]
level: practitioner
status: docs-checked
description: "Inject raw HTML with {@html}: XSS warning, valid standalone HTML requirement, no Svelte compilation, and styling the output with :global because scoped styles miss it."
sources:
  - https://raw.githubusercontent.com/sveltejs/svelte/main/documentation/docs/03-template-syntax/08-%40html.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```svelte
<article>
  {@html content}
</article>
```

Security: escape the string or only populate it with values under your control, to prevent XSS attacks. Never render unsanitized content.

Rules:
- The expression must be valid standalone HTML. `{@html '<div>'}content{@html '</div>'}` does not work because `</div>` alone is not valid HTML.
- It will not compile Svelte code.

Styling: the content is invisible to Svelte and gets no scoped styles, so this treats `a` and `img` as unused:

```svelte
<style>
  article {
    a { color: hotpink }
    img { width: 100% }
  }
</style>
```

Use the `:global` modifier to target everything inside the `<article>`:

```svelte
<style>
  article :global {
    a { color: hotpink }
    img { width: 100% }
  }
</style>
```

Related: `global-styles`.

## Checked

2026-11-08. Read the {@html} page in full. Removed an unsupported remark about plain `{expression}` being stringified and escaped; the rest matched.

Method: documentation only (raw page from the sveltejs/svelte repo); no commands were run.
