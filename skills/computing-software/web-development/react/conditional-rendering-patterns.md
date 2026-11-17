---
id: computing-software.web-development.react.conditional-rendering-patterns
name: conditional-rendering-patterns
category: computing-software
field: web-development
product: react
tags: [jsx, react-components, conditional-rendering, ternary-jsx, logical-and-zero-bug, early-return, null-rendering]
level: practitioner
status: verified
description: "Conditional rendering in React: early returns, ternaries, the && zero bug, mapping states to UI, and hiding vs unmounting (state loss and effects)."
sources:
  - https://react.dev/learn/conditional-rendering
  - https://react.dev/learn/preserving-and-resetting-state
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Conditional rendering patterns

**Goal:** readable conditional UI without rendering stray `0`s, losing state unexpectedly or nesting ternaries.

## 1. Patterns
```jsx
// early return for whole-component states
if (error) return <ErrorState error={error} />;
if (!data) return <Spinner />;

// either/or inline
{isEditing ? <Editor /> : <Preview />}

// optional element
{items.length > 0 && <List items={items} />}
```

## 2. The `&&` zero bug
`{count && <Badge count={count} />}` renders **`0`** when count is 0 (numbers are rendered; `false/null/undefined` aren't). Use a boolean: `{count > 0 && …}` or `{!!count && …}` or a ternary with `null`. `NaN` renders as the text `NaN` (both run on React 19.3.1).

## 3. Many states: a map, not nested ternaries
```jsx
const views = { idle: <Prompt />, loading: <Spinner />, error: <Retry onRetry={load} />, done: <Results data={data} /> };
return views[status];
```
Or a discriminated union in TypeScript with a `switch` in a helper - exhaustive checks catch missing states.

## 4. Unmount vs hide
- Conditional rendering **unmounts**: state inside is lost, effects clean up, and remounting refetches/re-initialises.
- Hiding with CSS (`hidden` attribute / `display:none`) keeps state and DOM (e.g. tab panels with form input you want to keep), at the cost of rendering all panels.
- React's `<Activity mode="hidden">` (new in React 19.2) hides the children with `display: none`, keeps their state, destroys their Effects and re-renders them at lower priority while hidden (react.dev Activity reference).
- Same component type at the same position keeps state across conditions: `{isA ? <Form key="a"/> : <Form key="b"/>}` needs different keys to reset.

## 5. Returning nothing
A component may return `null`. Prefer the parent deciding whether to render it when the condition is the parent's concern.

## Verify
- [ ] No stray `0` rendered when counts are zero (test with empty data).
- [ ] Switching tabs keeps or resets input state as intended.
- [ ] Every status value renders a defined view (TS exhaustiveness).
