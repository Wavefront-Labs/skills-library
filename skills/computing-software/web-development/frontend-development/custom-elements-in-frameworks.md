---
id: computing-software.web-development.frontend-development.custom-elements-in-frameworks
name: custom-elements-in-frameworks
category: computing-software
field: web-development
product: frontend-development
tags: [custom-elements-interop, web-components-react, iscustomelement, custom-elements-schema, web-components]
level: practitioner
status: docs-checked
description: "Using custom elements inside React 18/19, Vue and Angular: properties vs attributes, custom events, TypeScript JSX typings, compiler config and SSR caveats."
sources:
  - https://react.dev/reference/react-dom/components#custom-html-elements
  - https://vuejs.org/guide/extras/web-components
  - https://angular.dev/guide/components/advanced-configuration
  - https://lit.dev/docs/frameworks/react/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Custom elements in frameworks

The two recurring problems: passing rich data (objects, arrays, booleans) as **properties** not string attributes, and listening for **custom events**.

## 1. React
- **Current React docs**: values bound in JSX are passed as attributes by default, and non-string values are stringified (`[1,2,3]` arrives as `"1,2,3"`). React sets a property instead only when the property name exists on the element class during construction (for example initialised in the constructor). Listen for custom events with `on` plus the exact event name: `onspeak`, `onsay-hi` and `onsayHi` listen for `speak`, `say-hi` and `sayHi` (case and dashes are preserved).
- **Properties that React does not detect, or older React versions**: use a ref (works in every version):
```jsx
function Picker({ items, onChange }) {
  const ref = useRef(null);
  useEffect(() => { ref.current.items = items; }, [items]);
  useEffect(() => {
    const el = ref.current, h = e => onChange(e.detail);
    el.addEventListener("value-changed", h);
    return () => el.removeEventListener("value-changed", h);
  }, [onChange]);
  return <x-picker ref={ref} />;
}
```
- Or wrap once with `@lit/react` `createComponent({ tagName, elementClass, react: React, events: { onValueChanged: "value-changed" } })`.

## 2. Vue
```js
// vite.config.js
vue({ template: { compilerOptions: { isCustomElement: tag => tag.startsWith("x-") } } })
```
Vue 3 checks the `in` operator and sets a DOM property when the key exists on the element, else an attribute; force a property with `:items.prop="list"`. Events emitted by a custom element are listened to with `v-on` as usual. `defineCustomElement` turns Vue components into custom elements.

## 3. Angular
By default Angular throws on unknown elements; add `schemas: [CUSTOM_ELEMENTS_SCHEMA]` to the component's metadata to allow them (`NO_ERRORS_SCHEMA` allows any element and property).

## 4. SSR
Servers render the bare tag; the element upgrades after its definition loads. Avoid layout shift with `x-picker:not(:defined) { display: block; min-height: 40px; }`, or server-render declarative shadow DOM (Lit SSR).

## Gotchas
- Defining the element after the framework sets properties: the property lands on the un-upgraded element as an own property and shadows the class setter. Upgrade-safe elements re-read such properties in `connectedCallback` (the "lazy property" pattern).
- Framework re-renders may replace slotted light DOM; keep the element's own state in properties.

## Verify
- [ ] Test passing an array prop and receiving a custom event in your framework version.

## Checked

Checked 2026-10-26 against the react.dev reference (react-dom components, custom HTML elements), the Vue docs (Vue and Web Components), the Angular advanced component configuration guide and the Lit React wrapper docs.

- Fixed: React docs say values go in as attributes unless the property name exists on the class during construction, and give the event rule (`on` plus the exact event name); the old React 18 versus 19 split and the `className` claim were not in the docs and were removed.
- Fixed: Vue forces a property with `.prop`; the `^attr` form was not documented and was removed. Vue checks `in` before choosing a property.
- Removed: the TypeScript JSX typing snippet, the Angular binding syntax paragraph and the custom-elements-everywhere.com references, which could not be confirmed.
- Confirmed: Vue `isCustomElement` compiler option, `defineCustomElement`; Angular `CUSTOM_ELEMENTS_SCHEMA`; Lit `createComponent` with `tagName`, `elementClass`, `events`.

Method: documentation only; no commands were run.
