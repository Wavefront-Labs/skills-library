---
id: computing-software.web-development.react.props-and-children
name: props-and-children
category: computing-software
field: web-development
product: react
tags: [jsx, react-components, react-props, children-prop, prop-spreading, default-props, prop-types, typescript-props]
level: practitioner
status: verified
description: "Passing data into React components: props and destructuring defaults, children, spreading safely, render props vs elements as props, and typing props."
sources:
  - https://react.dev/learn/passing-props-to-a-component
  - https://react.dev/reference/react/Children
  - https://react-typescript-cheatsheet.netlify.app/docs/basic/getting-started/basic_type_example/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Props and children

**Goal:** component APIs that are easy to use, typed, and don't leak arbitrary attributes or re-render needlessly.

## 1. Destructure with defaults
```tsx
type ButtonProps = { variant?: 'primary' | 'ghost'; size?: 'sm' | 'md'; children: React.ReactNode } & React.ComponentPropsWithoutRef<'button'>;
export function Button({ variant = 'primary', size = 'md', children, className, ...rest }: ButtonProps) {
  return <button className={cx(styles[variant], styles[size], className)} {...rest}>{children}</button>;
}
```
- Default values in destructuring replace `defaultProps`, which React 19 removed for function components (upgrade guide). Checked on 19.3.1: with the automatic JSX runtime (`react/jsx-runtime`) `defaultProps` is ignored, but classic `React.createElement` still applies it, so do not rely on either; class components keep `defaultProps`.
- Props are read-only; never mutate them. Copy into state only for "initial value" semantics (`initialCount`), named accordingly.
- `ComponentPropsWithoutRef<'button'>` lets consumers pass `onClick`, `aria-*`, `type`; spread `...rest` **after** your defaults if you want consumers to override, before if you want to enforce.

## 2. children
`children` is whatever is between the tags: string, element, array, function, `null`. Treat it as opaque - `React.Children.map`/`cloneElement` are legacy-ish and break with fragments/wrappers. Prefer explicit props for named regions:
```tsx
<Card header={<h2>Orders</h2>} footer={<Pager />}>{rows}</Card>
```

## 3. Spreading pitfalls
- `{...props}` onto DOM elements forwards unknown props -> React warns "React does not recognize the `isActive` prop on a DOM element" (exact text from React 19.3.1) and leaks attributes. Destructure custom props out first.
- Spreading a fresh object/array prop (`style={{…}}`, `items={[…]}`) every render defeats `memo` on children - only matters if the child is memoised and expensive.

## 4. Passing components
Pass elements (`icon={<StarIcon />}`) rather than component types (`icon={StarIcon}`) unless the child must control props. Render props (`renderItem={(item) => <Row {...item} />}`) when the child supplies data.

## 5. Context vs props
Prop-drill 2-3 levels happily; reach for composition (pass children) before context. Context for truly global values (theme, user, locale).

## Verify
- [ ] TypeScript rejects invalid variants; consumers can pass aria/data attributes.
- [ ] No "unknown prop" warnings in the console.
- [ ] No component mutates its props (lint: `react/no-direct-mutation-state`, immutability review).
