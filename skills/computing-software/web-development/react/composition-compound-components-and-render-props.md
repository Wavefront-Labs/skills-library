---
id: computing-software.web-development.react.composition-compound-components-and-render-props
name: composition-compound-components-and-render-props
category: computing-software
field: web-development
product: react
tags: [jsx, react-components, compound-components, render-props, composition, slots-pattern, context-api, headless-components]
level: practitioner
status: docs-checked
description: "Composing React components: children and slot props, compound components sharing state via context, render props and headless hooks, and when each fits."
sources:
  - https://react.dev/learn/passing-props-to-a-component#passing-jsx-as-children
  - https://react.dev/reference/react/cloneElement#alternatives
  - https://react.dev/reference/react/createContext
  - https://www.radix-ui.com/primitives/docs/components/tabs
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Composition: compound components and render props

**Goal:** flexible components whose structure the consumer controls, without a prop for every variation ("prop explosion").

## 1. Start with children and slot props
```jsx
<Dialog title="Delete project" actions={<><Button>Cancel</Button><Button variant="danger">Delete</Button></>}>
  <p>This can't be undone.</p>
</Dialog>
```
Covers most cases and keeps data flow obvious.

## 2. Compound components (shared implicit state)
```jsx
const TabsCtx = createContext(null);
export function Tabs({ defaultValue, children }) {
  const [value, setValue] = useState(defaultValue);
  return <TabsCtx value={{ value, setValue }}>{children}</TabsCtx>;      // React 19: <Context> as provider
}
Tabs.List = ({ children }) => <div role="tablist">{children}</div>;
Tabs.Tab = ({ value, children }) => { const c = use(TabsCtx);
  return <button role="tab" aria-selected={c.value === value} onClick={() => c.setValue(value)}>{children}</button>; };
Tabs.Panel = ({ value, children }) => use(TabsCtx).value === value ? <div role="tabpanel">{children}</div> : null;

<Tabs defaultValue="a"><Tabs.List><Tabs.Tab value="a">A</Tabs.Tab><Tabs.Tab value="b">B</Tabs.Tab></Tabs.List>
  <Tabs.Panel value="a">…</Tabs.Panel><Tabs.Panel value="b">…</Tabs.Panel></Tabs>
```
Context (not `cloneElement`) lets parts be wrapped/nested freely; the React docs call `cloneElement` uncommon and fragile and list context among the alternatives. Throw a helpful error if a part is used outside its parent. Real tabs also need keyboard handling and id wiring - prefer a headless library (Radix, React Aria, Ark) that implements ARIA patterns.

## 3. Render props and headless hooks
```jsx
<Combobox items={users} renderItem={(u, { active }) => <UserRow user={u} highlighted={active} />} />
const { getInputProps, getItemProps, isOpen } = useCombobox({ items });   // headless hook: you render everything
```
Use when the child computes data the consumer renders. When consumers only need the logic, expose a custom hook instead.

## 4. Controlled and uncontrolled
Support both: `value`/`onValueChange` (controlled) and `defaultValue` (uncontrolled), the props Radix Tabs documents.

## 5. Avoid
`React.Children.map` + `cloneElement` to inject props (the React docs call both `Children` and `cloneElement` fragile), and boolean prop explosions (`showHeader`, `compact`, `withIcon`, `iconRight`…).

## Verify
- [ ] Parts work when wrapped in other elements/components.
- [ ] Both controlled and uncontrolled usage work.
- [ ] Keyboard/ARIA behaviour verified for widget-like compounds.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20) and the Radix website docs. Confirmed: React 19 lets you render `<SomeContext>` directly as the provider (createContext page); `cloneElement` and `Children` pages both call themselves uncommon and fragile and point to alternatives; Radix Tabs documents `defaultValue`, `value` and `onValueChange`. Removed the unconfirmed claim that hooks replaced most render-prop use and the wrapper/fragment breakage detail.

Method: documentation only; no commands were run.
