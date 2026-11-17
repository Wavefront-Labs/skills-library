---
id: computing-software.web-development.tailwind-css.tailwind-v4-custom-utilities-variants-and-plugins
name: tailwind-v4-custom-utilities-variants-and-plugins
category: computing-software
field: web-development
product: tailwind-css
tags: [tailwind, tailwind-plugins, at-utility, at-custom-variant, at-plugin, tailwind-v4, typography-plugin, web-development, tailwind-utility-directive, tailwind-variant-directive, tailwind-typography-plugin]
level: practitioner
status: verified
description: "Extending Tailwind v4 with @utility (static and functional), @custom-variant, @variant and @plugin, plus porting v3 JS plugins."
sources:
  - https://tailwindcss.com/docs/adding-custom-styles
  - https://tailwindcss.com/docs/functions-and-directives
  - https://tailwindcss.com/docs/plugins
  - https://github.com/tailwindlabs/tailwindcss-typography
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Custom utilities, variants and plugins in Tailwind v4

**Goal:** add project-specific utilities that behave like built-ins (variants, sorting, tree-shaking) instead of loose CSS classes.

## 1. Static utility
```css
@import "tailwindcss";

@utility content-auto {
  content-visibility: auto;
}
```
Usable as `content-auto`, `lg:content-auto`, `hover:content-auto`. Only emitted when used. A plain `.content-auto {}` class would not get variants.

## 2. Functional utility with `--value()`
```css
@theme { --tab-size-github: 8; }

@utility tab-* {
  tab-size: --value(--tab-size-*, integer, [integer]);
}
```
- `tab-github` resolves from the theme namespace, `tab-4` from bare integers, `tab-[12]` from arbitrary values.
- `--modifier()` reads the `/x` modifier (e.g. opacity-style).
- Within one `--value(a, b, c)` every form that resolves emits a declaration: with `--tab-size-4: 99` in `@theme`, `tab-4` compiled to `tab-size: 4; tab-size: var(--tab-size-4);`, so the later (theme) value wins in the cascade (run on 4.3.3). Across separate declarations, those that fail to resolve are omitted (docs).

## 3. Custom variants
```css
@custom-variant theme-midnight (&:where([data-theme="midnight"] *));
@custom-variant pointer-coarse (@media (pointer: coarse));
```
Then `theme-midnight:bg-black`, `pointer-coarse:p-4`. Use `:where()` to keep specificity at zero.

Apply a variant inside your own CSS:
```css
.prose-card { background: white; @variant dark { background: black; } }
```

## 4. Plugins
```css
@plugin "@tailwindcss/typography";
@plugin "@tailwindcss/forms";
@plugin "./plugins/brand.js";
```
v3-style JS plugins still load through `@plugin`:
```js
// plugins/brand.js
import plugin from "tailwindcss/plugin";
export default plugin(({ addUtilities, matchUtilities, addVariant, theme }) => {
  addVariant("hocus", ["&:hover", "&:focus-visible"]);
  matchUtilities({ "text-shadow": (v) => ({ textShadow: v }) },
                 { values: theme("textShadow") ?? { sm: "0 1px 1px rgb(0 0 0 / .2)" } });
});
```
Prefer the CSS-first `@utility`/`@custom-variant` for new work; reach for JS only for loops/computed values.

## 5. Gotchas
- `@utility` names must start with a lowercase letter and be alphanumeric (4.3.3 rejected `foo.bar` and accepted `foo_bar`); a functional one ends in `-*` with the `*` appearing once.
- Custom CSS in `@layer components` gets no variants (run: `md:card` generated nothing, and `.card` shipped although unused); move it to `@utility` if you need `md:` (`md:btn` worked).
- Plugin options: `@plugin "@tailwindcss/typography" { className: wysiwyg; }`.

## Verify
- [ ] `md:your-utility` and `hover:your-utility` produce CSS in the build output.
- [ ] Unused custom utilities are absent from production CSS.
- [ ] Custom variants have zero added specificity (inspect selector in DevTools).
