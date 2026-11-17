---
id: computing-software.web-development.react.typescript-with-react
name: typescript-with-react
category: computing-software
field: web-development
product: react
tags: [react, react-typescript, typescript, props-typing, event-types, generic-components, componentprops, web-development]
level: practitioner
status: docs-checked
description: "Typing React with TypeScript: props and children, events and refs, hooks, discriminated-union props, generic components and ComponentProps extension."
sources:
  - https://react.dev/learn/typescript
  - https://react.dev/blog/2024/04/25/react-19-upgrade-guide
  - https://github.com/DefinitelyTyped/DefinitelyTyped/blob/master/types/react/index.d.ts
  - https://github.com/typescript-cheatsheets/react
  - https://www.typescriptlang.org/tsconfig/#jsx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# TypeScript with React

**Goal:** types that catch misuse of components without fighting the compiler.

## 1. Props
```tsx
type ButtonProps = { variant?: "primary" | "ghost"; children: React.ReactNode } &
  React.ComponentPropsWithoutRef<"button">;
export function Button({ variant = "primary", children, ...rest }: ButtonProps) {
  return <button data-variant={variant} {...rest}>{children}</button>;
}
```
- Type props on the parameter, as the React docs do (`function MyButton({ title }: { title: string })`).
- `ComponentPropsWithoutRef<"button">` / `ComponentProps<typeof Other>` to extend native or existing components. React 19 with ref-as-prop: `ComponentProps<"button">` includes `ref`.
- `React.ReactNode` for anything renderable; `React.ReactElement` only when you must clone/inspect.

## 2. Events
```tsx
const onChange = (e: React.ChangeEvent<HTMLInputElement>) => setV(e.target.value);
const onSubmit = (e: React.FormEvent<HTMLFormElement>) => { e.preventDefault(); };
const onKey: React.KeyboardEventHandler<HTMLDivElement> = (e) => {};
```
Inline handlers infer types automatically - annotate only extracted functions.

## 3. Hooks
```tsx
const [user, setUser] = useState<User | null>(null);
const inputRef = useRef<HTMLInputElement>(null);          // DOM ref
const timer = useRef<number | undefined>(undefined);      // mutable value (React 19 requires an argument)
const [state, dispatch] = useReducer(reducer, initial);   // types flow from the reducer signature
const Ctx = createContext<Theme | null>(null);            // plus a guarded useTheme() hook
```

## 4. Discriminated-union props
```tsx
type Props =
  | { kind: "link"; href: string }
  | { kind: "button"; onClick: () => void };
function Action(p: Props) { return p.kind === "link" ? <a href={p.href} /> : <button onClick={p.onClick} />; }
```
Invalid combinations become compile errors.

## 5. Generic components
```tsx
type ListProps<T> = { items: T[]; getKey: (t: T) => string; render: (t: T) => React.ReactNode };
export function List<T>({ items, getKey, render }: ListProps<T>) {
  return <ul>{items.map(i => <li key={getKey(i)}>{render(i)}</li>)}</ul>;
}
```
In `.tsx`, arrow generics need `<T,>`.

## 6. Setup
Install `@types/react` and `@types/react-dom`; `dom` must be in `lib` and `jsx` must be set to a valid option (the React docs say `preserve` suffices for most apps; see the TypeScript `jsx` option for `react-jsx` and library publishing); enable `strict`. Validate external data at runtime (zod) - types don't check API responses.

## Verify
- [ ] `tsc --noEmit` passes in CI with `strict`.
- [ ] No `any` in component props (`grep -rn ": any" src/components`).
- [ ] Passing an invalid prop combination fails compilation (try it once).

## Checked

Checked 2026-10-25 against the React docs (react.dev repository, last commit 2026-10-20), the React 19 upgrade guide, the @types/react definitions (DefinitelyTyped, 19.x) and the typescript-cheatsheets repository. Confirmed: props typed on the parameter; `React.ChangeEvent`, `React.FormEvent`, `React.KeyboardEventHandler`, `React.ReactNode`, `React.ReactElement`, `ComponentProps` and `ComponentPropsWithoutRef` exist; `ComponentProps<"button">` includes `ref` (through `ClassAttributes`); `useRef` requires an argument in the React 19 types; `useState<User | null>` and `createContext<T | null>` patterns; the tsconfig requirements (`dom` in `lib`, a valid `jsx` option). Removed the `React.FC` history claim and the `"jsx": "react-jsx"` assertion.

Method: documentation only; no commands were run.
