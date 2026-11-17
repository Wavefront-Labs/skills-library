---
id: computing-software.web-development.tailwind-css.prettier-class-sorting-and-intellisense
name: prettier-class-sorting-and-intellisense
category: computing-software
field: web-development
product: tailwind-css
tags: [prettier-plugin-tailwindcss, tailwind-intellisense, tailwind-tooling, prettier, editor-setup]
level: intro
status: verified
description: "Setting up Tailwind tooling: prettier-plugin-tailwindcss class sorting, v4 stylesheet config, custom function attributes, VS Code IntelliSense settings and class-merging helpers."
sources:
  - https://github.com/tailwindlabs/prettier-plugin-tailwindcss
  - https://tailwindcss.com/docs/editor-setup
  - https://github.com/tailwindlabs/tailwindcss-intellisense
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Prettier class sorting and Tailwind IntelliSense

## 1. Class sorting
```bash
npm i -D prettier prettier-plugin-tailwindcss
```
```json
// .prettierrc
{
  "plugins": ["prettier-plugin-tailwindcss"],
  "tailwindStylesheet": "./src/styles/app.css",
  "tailwindFunctions": ["clsx", "cn", "cva", "tw"],
  "tailwindAttributes": ["containerClassName"]
}
```
- Sorts classes in the order Tailwind emits them (layout -> box -> typography -> variants), making diffs and duplicates obvious. Run (prettier 3.9.10, plugin 0.8.1, Tailwind 4.3.3): classes it does not know (`custom-thing`) are put first, `containerClassName` and `cn(...)` arguments were sorted, and `h-header` (from `@theme`) and `content-auto` (from `@utility`) sorted correctly only because `tailwindStylesheet` pointed at the CSS entry.
- v4: point `tailwindStylesheet` at the CSS entry with `@import "tailwindcss"` so custom `@theme` utilities sort correctly. v3: `tailwindConfig`.
- Must be the **last** plugin when combined with others (e.g. `prettier-plugin-svelte` first); for import-sorting plugins that conflict, use `prettier-plugin-merge` or check the README's compatibility list.
- Run in CI: `prettier --check .`

## 2. VS Code IntelliSense
Install "Tailwind CSS IntelliSense". Settings:
```json
{
  "files.associations": { "*.css": "tailwindcss" },
  "editor.quickSuggestions": { "strings": "on" },
  "tailwindCSS.classFunctions": ["cva", "cx", "cn", "clsx"],
  "tailwindCSS.experimental.configFile": "src/styles/app.css"
}
```
- Gives autocomplete, hover previews of generated CSS, colour swatches, and lint warnings for conflicting classes (`p-2 p-4`).
- Monorepos: set `experimental.configFile` to a map of stylesheet -> glob so each package gets its own theme.
- JetBrains IDEs have built-in Tailwind support; Neovim uses `tailwindcss-language-server`.

## 3. Merging conflicting classes
Sorting doesn't resolve conflicts from props. Use `tailwind-merge` in a `cn()` helper:
```ts
import { clsx, type ClassValue } from "clsx"; import { twMerge } from "tailwind-merge";
export const cn = (...i: ClassValue[]) => twMerge(clsx(i));
cn("px-2 py-1 bg-red-500", props.className);   // later px-4 wins cleanly
```
tailwind-merge v3 targets Tailwind v4; use v2 for Tailwind v3.

## Verify
- [ ] `prettier --check` passes in CI; IntelliSense resolves custom theme tokens; `cn()` calls get autocomplete.
