---
id: computing-software.web-development.react.children-api-and-cloneelement-pitfalls
name: children-api-and-cloneelement-pitfalls
category: computing-software
field: web-development
product: react
tags: [cloneelement, react-children, children-api, composition, react]
level: advanced
status: verified
description: "Why React docs discourage Children and cloneElement: fragile child inspection, alternatives with context, render props and explicit props, and safe uses when you can't avoid them."
sources:
  - https://react.dev/reference/react/Children
  - https://react.dev/reference/react/cloneElement
  - https://react.dev/reference/react/isValidElement
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# children, cloneElement and the Children API

`Children.map/count/toArray/only` and `cloneElement` are legacy APIs. They work on the **elements you were passed**, not on what renders, so they break as soon as someone wraps a child.

## 1. The fragility
```jsx
function Tabs({ children }) {
  return Children.map(children, (child, i) => cloneElement(child, { index: i, active: i === current }));
}
<Tabs>
  <Tab title="A" />
  <MyTab title="B" />        {/* wrapper component: receives props but may not forward them */}
  {cond && <Tab />}          {/* false still gets an index: Children.map calls you with null (cloneElement(null) throws) */}
  <>{list.map(...)}</>       {/* a Fragment counts as ONE child */}
</Tabs>
```
- Fragments aren't traversed (the React docs say so) and arrays are flattened. `Children.map`/`count` visit empty nodes (`null`, `undefined`, booleans) as one node each, with `null` passed to your callback, so `cloneElement(child)` throws "The argument must be a React element, but you passed null" (run on React 19.3.1); `Children.toArray` drops them.
- Injected props collide with props the user passed, and TypeScript can't see them.

## 2. Alternatives (preferred)
**Context for implicit state** (compound components):
```jsx
const TabsCtx = createContext(null);
function Tabs({ value, onChange, children }) { return <TabsCtx value={{ value, onChange }}>{children}</TabsCtx>; }
function Tab({ id, children }) {
  const { value, onChange } = use(TabsCtx);
  return <button role="tab" aria-selected={value === id} onClick={() => onChange(id)}>{children}</button>;
}
```
Works through any wrapper depth. (React 19 renders `<Context>` directly as a provider.)

**Data as props**: `<Tabs items={[{ id, title, content }]}>` - explicit, typeable, easy to index.

**Render props**: `<List items={rows} renderItem={(row, i) => <Row key={row.id} {...row} striped={i % 2} />} />`.

## 3. When it's still acceptable
- Wrapping each child in a layout element without changing it: `Children.map(children, c => <li>{c}</li>)` (a Fragment child is wrapped as one item, not traversed).
- `Children.only(children)` for components that require exactly one element (e.g. a Slot/`asChild` implementation); Radix's Slot uses `cloneElement` to merge props and refs - copy that well-tested implementation rather than writing your own.
- Counting for layout decisions where wrappers don't matter.

## 4. Merging when you clone
Merge, don't overwrite: compose event handlers (call both), combine `className`, merge refs (React 19 passes `ref` as a normal prop on function components).

## Verify
- [ ] Compound components work when children are wrapped in custom components and fragments; no props silently overwritten by cloneElement.
