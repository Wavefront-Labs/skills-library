---
id: computing-software.web-development.react.jsx-syntax-rules-and-fragments
name: jsx-syntax-rules-and-fragments
category: computing-software
field: web-development
product: react
tags: [jsx-syntax, react-fragments, jsx, classname, react]
level: intro
status: docs-checked
description: "Writing correct JSX: single root and fragments, keyed fragments, className and htmlFor, camelCase attributes, expressions vs statements, and common gotchas."
sources:
  - https://react.dev/learn/writing-markup-with-jsx
  - https://react.dev/learn/javascript-in-jsx-with-curly-braces
  - https://react.dev/reference/react/Fragment
  - https://react.dev/reference/react-dom/components/common
  - https://react.dev/learn/conditional-rendering
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# JSX rules and fragments

## 1. The three rules
1. **One root element** per returned expression. Wrap siblings in a fragment `<>...</>` rather than an extra `<div>` that breaks flex/grid layouts, tables and lists.
2. **Close every tag**: `<img />`, `<br />`, `<input />`.
3. **camelCase attributes**: `className`, `htmlFor`, `tabIndex`, `onClick`, `strokeWidth`. Exceptions: `aria-*` and `data-*` stay hyphenated.

## 2. Fragments with keys
```jsx
import { Fragment } from "react";
{terms.map(t => (
  <Fragment key={t.id}>        {/* short syntax <> can't take a key */}
    <dt>{t.term}</dt><dd>{t.definition}</dd>
  </Fragment>
))}
```

## 3. Curly braces
- `{}` holds **expressions**, not statements: use ternaries, `&&`, `.map()`, or compute before `return`.
- `style={{ marginTop: 8 }}`: outer braces = JS, inner = object; a number gets `px` appended unless the property is unitless.
- Strings: `title="Hello"`; dynamic: `title={`Hello ${name}`}`.

## 4. Gotchas
| Bug | Cause | Fix |
|---|---|---|
| A stray `0` renders | `{count && <Badge/>}` with count 0 | `{count > 0 && ...}` |
| Nothing renders | arrow with braces but no `return` | `() => (<li/>)` or add `return` |
| Error "Objects are not valid as a React child" | rendering a plain object | render its fields, or `JSON.stringify` for debugging |
| Attribute ignored | `class`, `for`, `onclick` | `className`, `htmlFor`, `onClick` |
| Handler fires on render | `onClick={save()}` | `onClick={save}` or `onClick={() => save(id)}` |

## 5. HTML injection
`dangerouslySetInnerHTML={{ __html: html }}` overrides the element's `innerHTML`. Unless the markup comes from a completely trusted source it is trivial to introduce an XSS hole. It cannot be combined with children; under Trusted Types pass a `TrustedHTML` value as `__html`.

## 6. Converting HTML
Paste-heavy migrations: use an HTML-to-JSX converter, then fix `style` strings to objects and inline event handlers to functions.

## Verify
- [ ] No React warnings about unknown DOM props or missing keys in the console; no stray `0`s in conditional rendering.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20). Confirmed: single root element and fragments; close every tag; camelCase attributes with `aria-*` and `data-*` kept hyphenated; keyed fragments need the explicit `<Fragment key>` form; double curly braces are an object in JSX; numeric style values get `px`; `dangerouslySetInnerHTML` shape, XSS warning and Trusted Types note; calling a handler (`onClick={f()}`) fires during render; a stray `0` from `count && ...` and the `count > 0 &&` fix; the HTML-to-JSX converter recommendation; plain objects as children raise "Objects are not valid as a React child". Removed the CSS custom property example, the whitespace and boolean-attribute rows, the comment syntax tip and the DOMPurify naming, which the docs do not cover.

Method: documentation only; no commands were run.
