---
id: computing-software.web-development.tailwind-css.shadcn-ui-and-headless-components
name: shadcn-ui-and-headless-components
category: computing-software
field: web-development
product: tailwind-css
tags: [shadcn-ui, headless-ui, radix-ui, component-libraries, tailwind-components]
level: practitioner
status: docs-checked
description: "Using shadcn/ui and headless libraries with Tailwind: the copy-in model and CLI, theming tokens, Radix primitives and asChild, the Base UI/React Aria options, and updating."
sources:
  - https://ui.shadcn.com/docs
  - https://ui.shadcn.com/docs/theming
  - https://headlessui.com/
  - https://www.radix-ui.com/primitives/docs/overview/introduction
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# shadcn/ui and headless component libraries

Headless libraries provide behaviour and accessibility (focus, keyboard, ARIA) without styles; Tailwind provides styling. shadcn/ui is a collection of such components copied into your repo.

## 1. shadcn/ui setup
```bash
npx shadcn@latest init        # writes components.json and sets up CSS variables
npx shadcn@latest add button dialog dropdown-menu form
```
- Components are copied into your project as **your code**: edit freely.
- Component docs offer Radix UI, Base UI and React Aria as the underlying primitive library; `cn()` combines `clsx` and `tailwind-merge`.
- Tailwind v4 projects use `@theme inline` with OKLCH CSS variables (`--primary`, `--background`, `--radius`) and `tw-animate-css` instead of `tailwindcss-animate`.

## 2. Theming
```css
:root { --primary: oklch(0.55 0.2 260); --primary-foreground: oklch(0.98 0 0); --radius: 0.5rem; }
.dark { --primary: oklch(0.7 0.15 260); }
@theme inline { --color-primary: var(--primary); --color-primary-foreground: var(--primary-foreground); }
```
Change tokens, not component files, for brand styling. Check contrast of every foreground/background pair.

## 3. Picking a headless library
- Radix Primitives: `asChild` lets a part render your own element instead of its default one.
- React Aria and Base UI: alternative primitive libraries offered by the shadcn component docs.
- Headless UI: Tailwind Labs headless component library (headlessui.com).

## 4. Keeping copied components current
Re-run `npx shadcn@latest add <component>` with `--diff` to see differences or `--overwrite` to replace existing files, on a branch, and merge your customisations. Keep customisations in wrappers where possible to reduce merge pain.

## 5. Pitfalls
- `asChild` requires your component to spread props onto its DOM node and forward its ref (Radix composition guide).

## Verify
- [ ] Components pass keyboard and screen-reader checks after theming; tokens drive light/dark via the `.dark` selector.

## Checked
2026-11-01. Confirmed against shadcn/ui docs (CLI add options --overwrite and --diff, Tailwind v4 page: @theme inline, OKLCH, tw-animate-css replacing tailwindcss-animate, theming page: :root and .dark tokens, button page: Radix UI, Base UI, React Aria) and the Radix composition guide (asChild, spread props, forward ref). Removed: the cva section and class-variance-authority claim, file paths, the comparison table rows for Ark/Zag, and the portal dark-mode pitfall.
Method: documentation only; no commands were run.
