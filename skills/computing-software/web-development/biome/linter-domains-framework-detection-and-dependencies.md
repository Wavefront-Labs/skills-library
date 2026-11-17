---
id: computing-software.web-development.biome.linter-domains-framework-detection-and-dependencies
name: linter-domains-framework-detection-and-dependencies
category: computing-software
field: web-development
product: biome
tags: [biome, domains, domain-detection, package-json-dependencies, react-domain, vue-domain, next-domain, solid-domain, svelte-domain, qwik-domain, astro-domain]
level: practitioner
status: docs-checked
description: "Which framework domains Biome enables from package.json dependencies (React, Vue, Next, Solid, Svelte, Qwik, Astro, Drizzle and more) and their version floors."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/linter/domains.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Each domain is switched on automatically when the nearest `package.json` declares a matching dependency at or above a version. Every domain accepts three config values: `"recommended"` (recommended non-nursery rules), `"all"` and `"none"`, under `linter.domains`.

Dependency triggers listed in the docs:
- Astro: `astro` >=1.0.0
- Drizzle: `drizzle-orm` >=0.9.0
- Next: `next` >=14.0.0
- Playwright: `@playwright/test` >=1.0.0
- Qwik: `@builder.io/qwik` >=1.0.0 or `@qwik.dev/core` >=2.0.0
- React: `react` >=16.0.0
- ReactNative: `react-native` >=0.60.0
- Solid: `solid` >=1.0.0
- Svelte: `svelte` >=3.0.0
- Tailwind: `tailwindcss` >=4.0.0
- TanstackQuery: `@tanstack/react-query`, `@tanstack/solid-query`, `@tanstack/svelte-query`, `@tanstack/vue-query` >=4.0.0 or `@tanstack/preact-query` >=5.0.0
- Test: `jest` >=26, `mocha` >=8, `ava` >=2, `vitest` >=1
- Turborepo: `turbo` >=1.0.0
- Vue: `vue` >=3.0.0

**Conflicts.** The React domain notes it may conflict with the Solid domain, and Solid notes it may conflict with React. Do not enable both blindly in one package.

**No recommended rules.** Astro, Svelte, Tailwind and TanstackQuery contain only nursery rules, so enabling the domain with `"recommended"` activates nothing; enable the individual rules.

**Example mix.** Next and React share `useExhaustiveDependencies` and `useHookAtTopLevel`; Qwik and Solid both include `noReactSpecificProps`; Svelte, Astro and Tailwind list rules for both JavaScript and HTML files.

Because this page is generated from Biome source, treat the exact rule lists as version-specific and confirm against the docs for your Biome version.

## Checked

2026-11-08. Read the domains page in full. Unchanged: dependency triggers and version floors, React and Solid conflict notes, nursery-only domains. Corrected the TanStack Query package names to their full scoped names and replaced an unsupported claim about Vue HTML rules. Removed: the invented Verify step.

Method: documentation only; no commands were run.
