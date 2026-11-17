---
id: computing-software.web-development.web-accessibility.duplicate-ids-and-aria-references
name: duplicate-ids-and-aria-references
category: computing-software
field: web-development
product: web-accessibility
tags: [duplicate-ids, aria-references, aria-labelledby, aria-describedby, wcag-4-1-2]
level: practitioner
status: verified
description: "Finding and fixing duplicate ids and broken ARIA id references: why they break names, component-generated ids, cross-shadow-root references and checks."
sources:
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://dequeuniversity.com/rules/axe/4.10/duplicate-id-aria
  - https://react.dev/reference/react/useId
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/ariaLabelledByElements
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Duplicate ids and broken ARIA references

`<label for>`, `aria-labelledby`, `aria-describedby`, `aria-controls`, `aria-activedescendant`, `aria-errormessage`, `headers` and skip links all point at ids. If the id is duplicated, the browser uses the first one in the document; if it's missing, the relationship silently disappears.

## 1. Typical causes
- Reusable components with hard-coded ids (`id="email"` in a form rendered twice, e.g. desktop and mobile copies).
- Lists rendering `id="item-title"` per row.
- Server templates and client hydration generating different ids.
- Ids referenced across shadow root boundaries (they don't resolve).
- Typos and ids removed during refactors while `aria-describedby` still points to them.

## 2. Generating ids
```jsx
function Field({ label, hint }) {
  const id = useId();                       // stable across SSR and hydration
  return (<>
    <label htmlFor={id}>{label}</label>
    <input id={id} aria-describedby={hint ? `${id}-hint` : undefined} />
    {hint && <p id={`${id}-hint`}>{hint}</p>}
  </>);
}
```
Vue 3.5+ (3.5.0 changelog): `useId()`; Svelte 5.20+: `$props.id()`; vanilla: a module counter or `crypto.randomUUID()` (not for SSR-hydrated markup). Only render `aria-describedby` when the target exists.

## 3. Shadow DOM
ARIA id references can't cross shadow boundaries. Options: keep label and control in the same root; use `ariaLabelledByElements`/`ariaDescribedByElements` element references (Baseline 2025, works across boundaries in some directions); or set `aria-label` on the host via ElementInternals.

## 4. Detection
- axe-core rules (4.13/4.14): `duplicate-id-aria` and `aria-valid-attr-value` (tags `wcag2a`, `wcag412`), `label`. The older `duplicate-id` rule is disabled and tagged `wcag2a-obsolete`.
- Nu HTML Checker reports all duplicate ids and `for` pointing to nothing.
- Quick console check:
```js
const ids = [...document.querySelectorAll("[id]")].map(e => e.id);
console.table(ids.filter((id, i) => ids.indexOf(id) !== i));
const refs = ["aria-labelledby", "aria-describedby", "aria-controls", "aria-errormessage", "aria-activedescendant", "for"];
document.querySelectorAll(refs.map(a => `[${a}]`).join(",")).forEach(el => {
  for (const a of refs) (el.getAttribute(a) ?? "").split(/\s+/).forEach(r => r && !document.getElementById(r) && console.warn("missing", a, r, el));
});
```
An earlier `??` chain version only checked the first attribute present on each element and missed `aria-controls="nope"` beside a valid `aria-describedby`; this loop checks every attribute. Run in Chromium: it reports the duplicate and each missing id, and a second `<label for="e">` still resolves `.control` to the first element with that id.

## Verify
- [ ] axe reports no duplicate-id-aria or invalid reference issues on every template; accessibility tree shows expected names and descriptions for repeated components.
