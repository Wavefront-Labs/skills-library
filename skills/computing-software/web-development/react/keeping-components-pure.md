---
id: computing-software.web-development.react.keeping-components-pure
name: keeping-components-pure
category: computing-software
field: web-development
product: react
tags: [jsx, react-components, pure-components, rules-of-react, idempotent-render, side-effects-in-render, strictmode]
level: practitioner
status: verified
description: "Writing pure React components per the Rules of React: no side effects or mutation during render, local mutation is fine, and how StrictMode surfaces impurity."
sources:
  - https://react.dev/learn/keeping-components-pure
  - https://react.dev/reference/rules
  - https://react.dev/reference/react/StrictMode
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Keeping components pure (Rules of React)

**Goal:** components return the same JSX for the same props/state/context, so React can render them twice, pause, resume or skip them (and the React Compiler can memoise them).

## 1. During render, don't
- Mutate props, state, context, or anything created outside the component (module variables, arrays passed in).
- Perform side effects: network requests, subscriptions, timers, `document.title =`, logging analytics, writing to localStorage.
- Read changing global values that aren't state (`Date.now()`, `Math.random()`, `window.innerWidth`) for output - results differ between renders and break hydration.
- Read or write `ref.current` (except lazy initialisation).

```jsx
let guestCount = 0;
function Guest() { guestCount++; return <p>Guest #{guestCount}</p>; }   // impure: output depends on how often React renders
function Guest({ n }) { return <p>Guest #{n}</p>; }                     // pure
```

## 2. Local mutation is fine
Creating and mutating objects inside the render (building an array with `push` before returning it) is pure - nobody else sees them.

## 3. Where side effects go
- **Event handlers** - user-caused effects (submit, click). They don't need to be pure.
- **Effects** (`useEffect`) - synchronising with external systems after render.
- **Server Components / loaders** - data fetching.

## 4. Other Rules of React
- Call hooks only at the top level of components/custom hooks (no conditions/loops).
- Never call component functions directly (`{Header()}`) - render them as `<Header />`.
- Don't mutate values after passing them to JSX or hooks (`useState`) - treat as immutable.

## 5. Tools
- `<StrictMode>` double-invokes components, initialisers, reducers and effects (setup/cleanup/setup) in development to expose impurity.
- `eslint-plugin-react-hooks` flags rule violations. Its React Compiler-powered rules (such as `purity`, `refs` and `immutability`) arrived in `recommended-latest` in 6.1.1 and are in `recommended` from 7.0.0 (plugin changelog); the Compiler skips components that break the rules.

## Verify
- [ ] Development StrictMode shows no duplicated side effects (double requests, double logs from render).
- [ ] Lint passes with the recommended react-hooks config.
- [ ] No hydration mismatch warnings from time/random values rendered on server and client.
