---
id: computing-software.web-development.react.error-boundaries
name: error-boundaries
category: computing-software
field: web-development
product: react
tags: [react, error-boundaries, react-error-boundary, getderivedstatefromerror, componentdidcatch, error-reporting, web-development]
level: practitioner
status: verified
description: "Containing render errors with React error boundaries: class implementation or react-error-boundary, placement, reset keys, reporting and what they don't catch."
sources:
  - https://react.dev/reference/react/Component#catching-rendering-errors-with-an-error-boundary
  - https://github.com/bvaughn/react-error-boundary
  - https://react.dev/reference/react-dom/client/createRoot#parameters
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Error boundaries

**Goal:** one broken widget shows a fallback instead of unmounting the whole app (React removes the entire tree on an uncaught render error).

## 1. Implementation
Still class-only in React:
```jsx
class ErrorBoundary extends React.Component {
  state = { error: null };
  static getDerivedStateFromError(error) { return { error }; }
  componentDidCatch(error, info) { reportError(error, info.componentStack); }
  render() { return this.state.error ? this.props.fallback : this.props.children; }
}
```
Most teams use `react-error-boundary`:
```jsx
<ErrorBoundary
  FallbackComponent={({ error, resetErrorBoundary }) => (
    <div role="alert"><p>Something went wrong.</p><button onClick={resetErrorBoundary}>Retry</button></div>
  )}
  onReset={() => queryClient.resetQueries()}
  resetKeys={[userId]}
>
  <Profile userId={userId} />
</ErrorBoundary>
```

## 2. What they catch
Errors thrown during render, in lifecycle methods, in constructors of children, and (React 18+) errors from Suspense data/`use` promises that reject.

Not caught (react.dev): event handlers (a throwing `onClick` leaves the boundary showing its children; checked), server-side rendering, errors thrown in the boundary itself, and async code such as `setTimeout` (an exception: errors thrown inside a `startTransition` are caught). Handle those with try/catch; to route an async error into a boundary, `setState(() => { throw err; })` or `showBoundary(err)` from `useErrorBoundary()` (both tested; `react-error-boundary` 6.1.6 also prefers `fallbackRender`, and `FallbackComponent`, `resetKeys` and `onReset` still work).

## 3. Placement
- Top-level boundary: friendly full-page error.
- Per route / per panel / per third-party widget so the rest stays usable.
- Pair with Suspense boundaries at the same granularity.

## 4. Reporting
React 19 root options centralise reporting:
```jsx
createRoot(el, {
  onCaughtError: (err, info) => Sentry.captureException(err, { extra: info }),
  onUncaughtError: (err, info) => Sentry.captureException(err),
});
```
In development React still logs caught errors to the console - expected.

## 5. Frameworks
Next.js: `error.tsx` per route segment is an error boundary (must be a client component); `global-error.tsx` for the root layout. React Router: `ErrorBoundary` route export.

## Verify
- [ ] Throw in a child component (temporary `throw new Error()`): fallback appears, rest of page works.
- [ ] Retry resets and re-renders successfully once the cause is fixed.
- [ ] Errors reach the error tracker with component stack.
