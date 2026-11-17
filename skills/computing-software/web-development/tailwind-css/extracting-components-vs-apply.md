---
id: computing-software.web-development.tailwind-css.extracting-components-vs-apply
name: extracting-components-vs-apply
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-apply, component-extraction, at-layer-components, maintainability, cva, web-development]
level: practitioner
status: verified
description: "Managing duplication in Tailwind: extract framework components or partials first, use @apply/@utility sparingly for third-party HTML, and avoid apply pitfalls."
sources:
  - https://tailwindcss.com/docs/styling-with-utility-classes#managing-duplication
  - https://tailwindcss.com/docs/functions-and-directives#apply-directive
  - https://tailwindcss.com/docs/adding-custom-styles#adding-component-classes
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Extracting components vs @apply

**Goal:** remove duplication without recreating a BEM stylesheet that drifts from the design system.

## 1. Order of preference
1. **Loop**: duplication in one file is often a list - render it with `map`/`v-for`/`{% for %}`.
2. **Multi-cursor edit**: a few identical siblings in one place are fine.
3. **Component/partial**: `<Button variant="primary">` in React/Vue/Svelte, a Blade/ERB/Django partial or include. Markup and classes stay together.
4. **@apply / @utility**: only when you don't control the HTML (CMS rich text, third-party widgets, Markdown output) or for tiny primitives repeated across templating languages.

## 2. Component with variants
```tsx
const styles = {
  base: "inline-flex items-center rounded-md px-4 py-2 font-medium focus-visible:outline-2",
  primary: "bg-blue-600 text-white hover:bg-blue-700",
  ghost: "bg-transparent hover:bg-gray-100",
};
export function Button({ variant = "primary", className = "", ...p }) {
  return <button className={`${styles.base} ${styles[variant]} ${className}`} {...p} />;
}
```
For many variants or override-safe merging use `cva` + `tailwind-merge`.

## 3. @apply when needed
```css
@layer components {
  .wysiwyg a { @apply text-blue-700 underline underline-offset-2 hover:text-blue-900; }
}
```
In v4, if the class should accept variants (`md:btn`), define it with `@utility btn { @apply ...; }` instead of `@layer components` (run on 4.3.3: `md:btn` compiled, `md:card` for a `@layer components` rule did not).

## 4. @apply pitfalls
- Component-scoped styles (Vue SFC `<style>`, CSS modules, Svelte) need `@reference "../app.css";` in v4 (run: without it the build failed with "Cannot apply unknown utility class `px-4`. Are you using CSS modules or similar and missing `@reference`?"; with it `@apply px-4 py-2 bg-brand tab-4` compiled).
- `@apply` copies declarations; it can't apply a class that only exists in another file's custom CSS unless it's a `@utility`.
- Applied classes lose the "see styles in markup" benefit and get no tree-shaking - the rule ships whether used or not.
- Ordering: applied utilities land where the rule is defined; a later utility class in markup still overrides in the utilities layer.

## 5. Typography for content
For CMS/Markdown HTML, `@tailwindcss/typography` (`prose prose-slate dark:prose-invert`) is usually better than hand-written `@apply` per tag.

## Verify
- [ ] `grep -rc "@apply" src` - each occurrence targets HTML you don't control.
- [ ] Shared UI exists once as a component; no copy-pasted 20-class strings across files.
- [ ] Component accepts `className` and overrides resolve predictably.
