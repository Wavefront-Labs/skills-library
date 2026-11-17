---
id: creative-arts.design-for-form-and-experience.design-systems.documenting-components-in-storybook-and-a-docs-site
name: documenting-components-in-storybook-and-a-docs-site
category: creative-arts
field: design-for-form-and-experience
product: design-systems
tags: [storybook, documentation-site, component-docs, storybook-docs, mdx, design-system-site, docusaurus]
level: practitioner
status: draft
description: "Document components with Storybook (CSF stories, autodocs, controls, a11y addon, MDX) and publish a docs site with search, versioning, tokens and design guidance."
sources:
  - "Storybook docs (storybook.js.org/docs)"
  - "Storybook - Autodocs and Component Story Format 3 (storybook.js.org/docs/writing-docs/autodocs)"
  - "Docusaurus / Zeroheight documentation platforms (docusaurus.io, zeroheight.com)"
licence: Apache-2.0
version: 2
updated: 2026-11-17
---

# Storybook component docs and a documentation site

## Storybook setup
```bash
npx storybook@latest init
```
- **Stories** in CSF 3: `export default { title: 'Components/Button', component: Button, tags: ['autodocs'] }` and named exports with `args`; one story per variant and state (Default, Disabled, Loading, Error).
- **Autodocs** generate a docs page from props types (TypeScript) and JSDoc comments; add `argTypes` descriptions and `controls` so users can play with props.
- **MDX** docs for narrative pages (principles, usage), embedding live stories with `<Canvas>` and `<Controls>`.
- **Addons:** `@storybook/addon-a11y` (axe checks per story), `addon-interactions` (play functions and tests), `addon-viewport`, `addon-themes` (light/dark), Figma embed addon linking the design.
- **Test:** `test-runner` or Vitest integration to run stories as tests in CI; Chromatic for visual review (`creative-arts.design-for-form-and-experience.design-systems.visual-regression-testing-for-components`).

## Publishing
- Deploy Storybook as static files (`storybook build`) per version/branch; put it behind the docs site.
- A **documentation site** (Docusaurus, Zeroheight, Supernova, or a custom Astro/Next site) holds foundations (colour, type, spacing, tokens), usage guidance (`creative-arts.design-for-form-and-experience.design-systems.writing-component-usage-guidelines`), content and accessibility guides, and a **changelog** and roadmap.
- Provide **search** (Algolia DocSearch or Pagefind), copy-paste code, install instructions, and a version switcher.
- Single source: generate token tables and prop tables from the code and token files to avoid drift.

## Gotchas
- Docs that are separate from code rot; make stories the source of truth.
- Include accessibility and responsive stories, not just happy paths.

## Verify
- [ ] Each component has stories for all variants and states, with controls.
- [ ] A11y checks and tests run in CI.
- [ ] Site has search, versioning and generated token/prop tables.
