---
id: computing-software.web-development.react.upgrading-to-react-19
name: upgrading-to-react-19
category: computing-software
field: web-development
product: react
tags: [react-19-upgrade, react-codemod, removed-apis, types-react-codemod, react-upgrade, react]
level: practitioner
status: verified
description: "Upgrading an app to React 19: go via 18.3 warnings, run the codemods, replace removed APIs (render, propTypes, string refs, findDOMNode), TypeScript changes and error handling."
sources:
  - https://react.dev/blog/2024/04/25/react-19-upgrade-guide
  - https://github.com/reactjs/react-codemod
  - https://github.com/eps1lon/types-react-codemod
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Upgrading to React 19

## 1. Order of work
1. Upgrade to **React 18.3** first: same as 18.2 plus deprecation warnings for everything removed in 19. Fix warnings.
2. Ensure the new JSX transform is enabled (required in 19).
3. `npm i react@^19 react-dom@^19 @types/react@^19 @types/react-dom@^19`.
4. Run codemods:
```bash
npx codemod@latest react/19/migration-recipe        # replace-reactdom-render, replace-string-ref, replace-act-import, replace-use-form-state, prop-types-typescript
npx types-react-codemod@latest preset-19 ./src
```
5. Upgrade libraries that pin React 18 (testing-library, router, UI kits); check peer dependency warnings.

## 2. Removed APIs and replacements
| Removed | Use |
|---|---|
| `ReactDOM.render` / `hydrate` | `createRoot().render` / `hydrateRoot` |
| `unmountComponentAtNode` | `root.unmount()` |
| `findDOMNode` | refs |
| `propTypes` on function components, `defaultProps` on functions | TypeScript, default parameters |
| legacy context (`contextTypes`), string refs | `createContext`, callback/object refs |
| `react-dom/test-utils` `act` | `import { act } from "react"` |
| `react-test-renderer/shallow` | `react-shallow-renderer` package (the guide's drop-in) or, preferably, Testing Library |

## 3. TypeScript changes
- `useRef()` requires an argument; refs are mutable by default (`useRef<T>(null)` gives `RefObject<T | null>`).
- Ref callbacks may return a cleanup function, so implicit returns (`ref={el => (this.el = el)}`) become type errors: use a block body.
- Global `JSX` namespace removed: use `React.JSX`.
- `ReactElement` props default to `unknown` instead of `any`.

## 4. Behaviour changes
- Errors during render are no longer re-thrown; use root options `onUncaughtError`, `onCaughtError` for reporting.
- `ref` is a regular prop on function components (forwardRef still works, later deprecated).
- StrictMode reuses memoised results on the second render; Suspense pre-warms siblings differently.
- `<Context>` can be used as a provider directly.

## Verify
- [ ] No React warnings in the console with 18.3 before switching; test suite and type-check pass on 19; error reporting still receives render errors.
