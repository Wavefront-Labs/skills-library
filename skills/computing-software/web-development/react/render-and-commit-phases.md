---
id: computing-software.web-development.react.render-and-commit-phases
name: render-and-commit-phases
category: computing-software
field: web-development
product: react
tags: [render-and-commit, react-rendering, reconciliation, re-render, react]
level: practitioner
status: docs-checked
description: "How React renders: triggers, the render phase calling components, the commit phase updating the DOM, why re-render does not mean DOM change, and the rules this imposes on code."
sources:
  - https://react.dev/learn/render-and-commit
  - https://react.dev/learn/keeping-components-pure
  - https://react.dev/learn/preserving-and-resetting-state
  - https://react.dev/reference/react/useLayoutEffect
  - https://react.dev/reference/react/useRef
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Render and commit phases

## 1. Three steps
1. **Trigger**: initial `root.render()`, or a state update (`setState`, `dispatch`, context value change, external store change via `useSyncExternalStore`). Parent re-render re-renders children by default.
2. **Render**: React calls your component functions to compute the new JSX tree and diffs it with the previous one (reconciliation). Pure computation - nothing touches the DOM.
3. **Commit**: React applies the minimal DOM changes; layout effects (`useLayoutEffect`) run before the browser repaints, and `useEffect` Effects run after the commit without blocking the paint.

## 2. Consequences
- A re-render does not mean the DOM changed. If output is identical, commit does nothing. Optimise only when the **render work itself** is expensive (profiler) or causes heavy child trees to re-render.
- Render can happen more than once per commit or be discarded (StrictMode double-invokes in dev; concurrent rendering may interrupt and restart transitions). So render must be **pure**: the same inputs give the same output, and nothing that existed before the call is mutated.
- Side effects belong in event handlers (preferred) or effects (synchronising with external systems).
- Do not read or write `ref.current` during rendering (except for initialisation); it makes behaviour unpredictable.
- State updates are batched and applied on the next render: `setCount(count + 1)` twice still adds 1 (use the updater `c => c + 1`).

## 3. Identity and reconciliation
React matches elements by **type + position** (or `key`). Same type at same position -> update, state preserved. Different type -> unmount subtree, state lost. Defining a component inside another component creates a new type each render -> its state resets every render.

## 4. Inspecting
- React DevTools Profiler: "Highlight updates when components render", and per-commit flamegraph with "why did this render".
- `<Profiler onRender>` API for measuring render duration programmatically.
- React Compiler (stable) auto-memoises to skip unnecessary re-renders; it relies on the purity rules above.

## Verify
- [ ] Components produce the same output for the same inputs; no side effects during render (StrictMode double render shows no duplicated effects/requests); no components defined inside other components.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20). Confirmed: trigger, render and commit steps and the browser paint epilogue; components must be pure (do not change objects that existed before the call; same inputs, same output); Strict Mode renders components twice in development; state updates are queued so `setNumber(number + 1)` three times adds one; a different component type at the same position resets state and nested component definitions reset state; `useLayoutEffect` fires before the browser repaints; `ref.current` must not be read or written during render. Removed the "refs are set during commit" detail and the Math.random/Date.now/network examples, which the docs do not state.

Method: documentation only; no commands were run.
