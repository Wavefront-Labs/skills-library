---
id: computing-software.web-development.react.profiling-and-memoisation
name: profiling-and-memoisation
category: computing-software
field: web-development
product: react
tags: [react, react-profiler, react-memo, usememo, usecallback, react-compiler, why-did-you-render, performance, web-development]
level: practitioner
status: docs-checked
description: "Finding and fixing slow React renders: React DevTools Profiler, Profiler API, memo/useMemo/useCallback used correctly, and what React Compiler changes."
sources:
  - https://react.dev/reference/react/Profiler
  - https://react.dev/reference/dev-tools/react-performance-tracks#using-profiling-builds
  - https://react.dev/reference/react/memo
  - https://react.dev/reference/react/useMemo
  - https://react.dev/learn/react-compiler/installation
  - https://github.com/GoogleChrome/web-vitals
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Profiling and memoisation

**Goal:** measure first, then memoise only what the profiler shows is expensive.

## 1. Profile
- React DevTools > Profiler: record an interaction, check the flame chart for components with long render times and the reason for each render (enable "Record why each component rendered while profiling" in the Profiler settings).
- Settings > "Highlight updates when components render" to spot cascades.
- Profile a production build with profiling enabled (alias `react-dom/client` to `react-dom/profiling` at build time) for realistic numbers; profiling is disabled in plain production builds.
- Programmatic: `<Profiler id="Feed" onRender={(id, phase, actualDuration) => ...}>`.

## 2. Common causes
- Parent state changes re-render all children (default React behaviour).
- New object/array/function props each render break child `memo`.
- Context value recreated each render.
- Expensive calculations in render (sorting/filtering thousands of rows).
- Rendering 5,000 DOM rows - virtualise instead (`@tanstack/react-virtual`).

## 3. Tools, used correctly
```jsx
const Row = memo(function Row({ item, onSelect }) { ... });
const sorted = useMemo(() => items.toSorted(byDate), [items]);
const onSelect = useCallback(id => setSelected(id), []);
```
- `memo` skips re-render when props are shallowly equal - useless if a prop is a fresh object each time.
- `useMemo` for expensive computations or to stabilise a value passed to a memoised child/effect deps.
- `useCallback` only matters when the function is passed to a memoised child or used in deps.
- Better first: move state down (into the component that uses it), or lift content up (`children` prop) so it doesn't re-render.

## 4. React Compiler
React Compiler (stable; installed as `babel-plugin-react-compiler`; best with React 19, and 17 and 18 are supported with `react-compiler-runtime`) auto-memoises components and values. With it on, most manual `memo/useMemo/useCallback` becomes unnecessary; code must follow the Rules of React. Keep the profiler workflow - it doesn't fix O(n²) algorithms or huge DOM.

## 5. Measure user impact
Check INP in the field (web-vitals `onINP`) and long tasks in the Performance panel; a component that takes negligible time isn't worth memoising.

## Verify
- [ ] Before/after Profiler recordings show reduced commit duration for the target interaction.
- [ ] Memoised children no longer appear as rendered in the target interaction.
- [ ] No memoisation added without a recorded reason.

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the React DevTools source and the web-vitals README. Confirmed: `<Profiler id onRender>` with `onRender(id, phase, actualDuration, ...)`; profiling is disabled in production builds and is enabled by aliasing `react-dom/client` to `react-dom/profiling`; `memo` shallow prop comparison; the DevTools settings "Highlight updates when components render" and "Record why each component rendered while profiling"; React Compiler is stable, installs as `babel-plugin-react-compiler` and supports React 17 and 18 with `react-compiler-runtime`; web-vitals exports `onINP`. Removed the "several times slower" and "2ms" figures, the compiler 1.0 label and the grey flame chart detail.

Method: documentation only; no commands were run.
