---
id: computing-software.web-development.tailwind-css.state-variants-group-peer-has-data
name: state-variants-group-peer-has-data
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, group-peer, data-attribute-variants, aria-variants, has-variant, focus-visible, state-variants, web-development, group-hover, peer-variant]
level: practitioner
status: verified
description: "Styling interactive state in Tailwind: hover/focus-visible, named group and peer, has-*, data-* and aria-* variants, not-*, in-* and ordering rules."
sources:
  - https://tailwindcss.com/docs/hover-focus-and-other-states
  - https://tailwindcss.com/docs/upgrade-guide
  - https://developer.mozilla.org/en-US/docs/Web/CSS/:has
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# State variants: group, peer, has, data-* and aria-*

**Goal:** drive styles from real DOM/ARIA state so visuals and accessibility can't drift apart.

## 1. Focus done right
```html
<button class="rounded-md bg-blue-600 px-4 py-2 hover:bg-blue-700 focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-blue-600 disabled:opacity-50">
```
Use `focus-visible:` for rings (keyboard only), not `focus:`. Never remove outlines without a replacement.

## 2. Parent state: group (named when nested)
```html
<a class="group/card ...">
  <h3 class="group-hover/card:underline">Title</h3>
  <ul class="group/item"><li class="group-hover/item:visible invisible">...</li></ul>
</a>
```
Unnamed `group` + nested `group` = ambiguous; name them.
v4 `in-*` variant: `in-focus:opacity-100` reacts to any ancestor state without a `group` class.

## 3. Sibling state: peer
```html
<input type="email" class="peer" required />
<p class="invisible peer-invalid:visible peer-placeholder-shown:invisible">Enter a valid email</p>
```
`peer` only works for **later** siblings (CSS `~` combinator). Put the peer first in the DOM.

## 4. has-* (parent reacts to children)
```html
<label class="rounded-lg border has-[:checked]:border-blue-600 has-[:checked]:bg-blue-50">
  <input type="radio" name="plan" class="sr-only" /> Pro
</label>
```
`group-has-[img]:`, `peer-has-*` also exist. `:has()` is Baseline 2023.

## 5. data-* and aria-* (component libraries)
Headless libraries (Radix, Headless UI, React Aria) expose state as attributes:
```html
<div data-state="open" class="data-[state=open]:animate-in data-[state=closed]:hidden"></div>  <!-- animate-in is not core: it needs a plugin such as tw-animate-css -->
<button aria-expanded="true" class="aria-expanded:rotate-180"></button>
<th aria-sort="ascending" class="aria-[sort=ascending]:text-blue-600"></th>
<div data-active class="data-active:font-bold"></div>  <!-- v4 bare boolean attribute -->
```
Prefer styling `aria-*` you must set anyway over parallel `isOpen ? 'rotate-180' : ''` class logic.

## 6. Other useful variants
`not-[:first-child]:mt-2`, `not-disabled:hover:` (v4 `not-*`), `open:` (details/dialog), `*:` direct children, `first:`/`last:`/`odd:`, `invalid:`/`user-invalid:` (after interaction), `starting:` (`@starting-style`), `inert:`.

## 7. Ordering
v4 applies stacked variants left to right like nested selectors (run: `dark:md:hover:underline` compiled to nested `prefers-color-scheme`, `width >= 48rem` and `hover: hover` at-rules; `aria-expanded:` matches `[aria-expanded="true"]`, `peer-*` uses the `~` sibling combinator). `dark:md:hover:` all compose; write them consistently and let the Prettier plugin (`prettier-plugin-tailwindcss`) sort classes.

## Verify
- [ ] Keyboard Tab shows a visible focus ring on every interactive element; mouse click doesn't.
- [ ] Peer elements precede their dependents in the DOM.
- [ ] Toggling `aria-expanded`/`data-state` in DevTools updates styles with no JS class changes.
