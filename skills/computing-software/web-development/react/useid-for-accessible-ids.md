---
id: computing-software.web-development.react.useid-for-accessible-ids
name: useid-for-accessible-ids
category: computing-software
field: web-development
product: react
tags: [useid, react-hooks, accessible-ids, aria-describedby, ssr-hydration, react]
level: practitioner
status: verified
description: "Generating stable, hydration-safe ids with useId for label/aria associations, deriving multiple ids, identifierPrefix for multiple roots, CSS selector caveats and misuse."
sources:
  - https://react.dev/reference/react/useId
  - https://react.dev/reference/react-dom/client/createRoot#parameters
  - https://www.w3.org/WAI/tutorials/forms/labels/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# useId for accessible ids

## 1. Use
```jsx
function EmailField({ error }) {
  const id = useId();
  return (
    <>
      <label htmlFor={`${id}-input`}>Email</label>
      <input id={`${id}-input`} type="email" aria-describedby={error ? `${id}-err` : undefined} aria-invalid={!!error} />
      {error && <p id={`${id}-err`}>{error}</p>}
    </>
  );
}
```
One `useId()` per component; derive suffixes for related elements. The id is unique per component instance and identical on server and client, so SSR hydration does not mismatch (unlike `Math.random()` or module counters).

## 2. Do not
- Use it for list `key`s (keys come from data).
- Hard-code ids in reusable components (two instances = duplicate ids = broken labels).
- Rely on its format: it is an implementation detail and has changed between React versions; React 19.3.1 produced `_r_0_` (and `_app-r_1_` with `identifierPrefix: "app-"`), and 19.2 changed the default prefix; it may contain characters that need escaping in selectors: `document.querySelector("#" + CSS.escape(id))`. Prefer refs over querying by id.

## 3. Multiple React roots / micro-frontends
Ids are unique within a root. With several roots on one page, set a prefix:
```js
createRoot(el, { identifierPrefix: "checkout-" });
hydrateRoot(el, <App />, { identifierPrefix: "checkout-" });   // must match the server's prefix
```

## 4. Before useId
Class components or React < 18: generate ids in a library (`@reach/auto-id`, `react-aria`'s `useId`) or pass ids as props.

## Verify
- [ ] Rendering the component twice yields distinct ids; clicking each label focuses its own input; no hydration warnings.
