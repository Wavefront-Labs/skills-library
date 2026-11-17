---
id: computing-software.devops-ci-cd.turborepo.env-framework-inference-prefix-table
name: env-framework-inference-prefix-table
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, framework-inference, env-wildcards, next-public, vite-prefix, framework-inference-false, negative-wildcard, per-package]
level: practitioner
status: docs-checked
description: "Turborepo auto-adds env wildcards for known frameworks such as NEXT_PUBLIC_* and VITE_*; inference is per package and can be disabled."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Turborepo automatically adds prefix wildcards to your `env` key for common frameworks, so variables with these prefixes need not be listed in packages that use them:

- Next.js: `NEXT_PUBLIC_*`
- Vite: `VITE_*`
- Create React App: `REACT_APP_*`
- Gatsby: `GATSBY_*`
- Nuxt: `NUXT_*`, `NUXT_ENV_*`
- Expo: `EXPO_PUBLIC_*`
- Astro: `PUBLIC_*`
- SvelteKit: `PUBLIC_*`
- Remix: `REMIX_*`
- SolidStart: `VITE_*`
- RedwoodJS: `REDWOOD_ENV_*`
- Sanity: `SANITY_STUDIO_*`

**Framework inference is per package**, so a package using Next.js gets the Next wildcard but not others.

**Opting out:**
- run tasks with `--framework-inference=false`, or
- add a negative wildcard to the `env` key, for example `"env": ["!NEXT_PUBLIC_*"]`.

The `--framework-inference` flag is among the flag values that feed the global hash (see the caching hash inputs skill).

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: a long unsourced paragraph about the configuration reference and the Verify step.

Method: documentation only; no commands were run.
