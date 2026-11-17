---
id: computing-software.web-development.hono.hono-css-helper
name: hono-css-helper
category: computing-software
field: web-development
product: hono
tags: [hono, helper, css, jsx, styling]
level: practitioner
status: docs-checked
description: "Style Hono JSX with the experimental hono/css helper: css, cx, keyframes, Style, global styles, CSP nonce, createCssContext and injection risks."
sources:
  - https://github.com/honojs/website/blob/main/docs/helpers/css.md
  - https://github.com/honojs/website/blob/main/docs/middleware/builtin/secure-headers.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# CSS helper (experimental)

Import: `import { css, cx, keyframes, Style, createCssContext } from 'hono/css'`.

`css` is a template literal that returns a class name; `<Style />` outputs the collected CSS and must be included (the page's example puts it inside `<head>`).

```tsx
app.get('/', (c) => {
  const headerClass = css`
    background-color: orange;
    color: white;
    padding: 1rem;
  `
  return c.html(
    <html>
      <head><Style /></head>
      <body><h1 class={headerClass}>Hello!</h1></body>
    </html>
  )
})
```

- Pseudo-classes use nesting: `&:hover { background-color: red; }`.
- Extend by embedding a class: `` css`${baseClass} font-size: 3rem;` ``; nest with `${headerClass} { h1 { ... } }`.
- Global styles: `:-hono-global { html { font-family: Arial, Helvetica, sans-serif; } }`, or `<Style>{css`html { ... }`}</Style>`.
- `keyframes`: `const fade = keyframes`from {opacity:0} to {opacity:1}``, then `animation-name: ${fade};`.
- `cx(buttonClass, primaryClass)` composes class names, or `cx('h1', primaryClass)`.

## With a CSP nonce
Set `styleSrc: [NONCE]` in `secureHeaders` and render `<Style nonce={c.get('secureHeadersNonce')} />`.

## createCssContext
`const { css, cx, keyframes, Style } = createCssContext({ id: 'my-app' })` customises the style element ID. `classNameSlug: (hash, label, css) => label ? `h-${label}` : hash` renames classes (label comes from a leading `/* comment */`). `onInvalidSlug: (slug) => { throw new Error(...) }` replaces the default warning.

## Gotcha: raw CSS
Interpolated values are inserted as raw CSS. HTML breakouts (quotes, backslashes, `</`) are blocked but `{`, `}` and `;` pass through, allowing CSS injection. Validate untrusted input against an allowlist first (`ALLOWED_COLORS.includes(input) ? input : 'black'`).

## Checked

2026-11-04. Read in full from the honojs/website docs repository: docs/helpers/css.md, docs/middleware/builtin/secure-headers.md. Confirmed against the page: every parameter name, default, import path, option value and code example left in this skill. Removed: the invented Verify step (curl/tsc/browser checks the page does not describe); the "must be in head" requirement (the page only shows it there).

Method: documentation only; no commands were run.
