---
id: computing-software.web-development.tailwind-css.css-architecture-bem-modules-css-in-js
name: css-architecture-bem-modules-css-in-js
category: computing-software
field: web-development
product: tailwind-css
tags: [css-modules, css-in-js, css-architecture, vanilla-extract]
level: practitioner
status: docs-checked
description: "Scoping CSS to avoid collisions: how CSS Modules and zero-runtime vanilla-extract work, with what each guarantees and exports."
sources:
  - https://github.com/css-modules/css-modules
  - https://vanilla-extract.style/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CSS architecture: CSS Modules and vanilla-extract

**Goal:** pick a styling approach that prevents collisions and scales with the team, without paying runtime costs you do not need.

## 1. CSS Modules
- A CSS Module is a CSS file where all class names and animation names are scoped locally by default. `url(...)` and `@import` use module request format (`./xxx` relative, `xxx` from the modules folder such as node_modules).
- Written like normal CSS and compiled to a low-level interchange format called ICSS.
- Importing from JavaScript exports an object mapping local names to global names:
```js
import styles from './style.css';
element.innerHTML = '<div class="' + styles.className + '">';
```
- Stated benefits: local scope prevents clashes across parts of a project; importing styles into components makes dependencies clear; the same class names can be used in different modules.
- The repository documents composition, local scope, pseudo class selectors and theming.

## 2. vanilla-extract (zero-runtime)
- "Zero-runtime Stylesheets-in-TypeScript": write type-safe, locally scoped classes, variables and themes in TypeScript, and static CSS files are generated at build time. The site's pitch: no dynamic CSS engine shipped to users.
- Supports variables, selectors, pseudo-classes, media/feature/container queries, keyframes, font-face and global styles.
- Theming via `createTheme` with type-safe token contracts; `createVar` for CSS variables; `styleVariants` for named variant collections.
- Official integrations: webpack, esbuild, Vite and Next.js. Extension libraries named on the site: Sprinkles, Recipes, Dessert Box.

## 3. Choosing
Prefer approaches that resolve to static CSS at build time (CSS Modules, vanilla-extract) when you want collision-free scoping with no runtime style engine. The cited pages do not compare against BEM, utility-first or runtime CSS-in-JS.

## Verify
- [ ] No two components can collide on a class name (build-time scoping).
- [ ] Production output contains generated CSS files rather than a style-injection runtime.

## Checked
Method: docs-only read on 2026-11-09 of the css-modules README and the vanilla-extract home page, in full via text extraction. Dropped sources: getbem.com (page text unreadable) and react.dev style reference (not relevant to the claims kept). Removed as unstated: BEM rules, comparison table, runtime CSS-in-JS and React Server Components claims, INP and hydration claims, composes/:global code, cascade-layer and stylelint advice, and the tags css-cascade, specificity, bem, styled-components and scoped-css.
