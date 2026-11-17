---
id: computing-software.web-development.storybook.environment-variables
name: environment-variables
category: computing-software
field: web-development
product: storybook
tags: [env-vars, storybook-prefix, dotenv, import-meta-env, process-env]
level: practitioner
status: docs-checked
description: "Expose environment variables to stories with the STORYBOOK_ prefix, .env files and the env main config option."
sources:
  - https://storybook.js.org/docs/configure/environment-variables
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Environment variables

Goal: pass configuration into stories safely.

Variables prefixed with `STORYBOOK_` are available as `process.env.STORYBOOK_*` with Webpack and `import.meta.env.STORYBOOK_*` with Vite:

```shell
STORYBOOK_THEME=red STORYBOOK_DATA_KEY=12345 npm run storybook
```

```ts
console.log(import.meta.env.STORYBOOK_THEME);
```

- `.env` files work: put `STORYBOOK_DATA_KEY=12345` in `.env`, or use `.env.development` / `.env.production` for modes.
- In `preview-head.html` and `preview-body.html` use substitution `%STORYBOOK_THEME%`; add quotes where the value needs them.
- With Vite, Node globals like `process.env` are not provided; use `import.meta.env`.
- Variables are embedded into the build, so anyone can read them. Never put secrets or private API keys in them.
- Values given at `storybook build` time are hardcoded into the static output.
- Alternatively use the `env` field in `main.ts`:

```ts
env: (config) => ({ ...config, EXAMPLE_VAR: 'Example var' }),
```

Verify: the variable value prints in the browser console from a story.

## Checked
Date: 2026-11-04. Read the Environment variables page (storybookjs/storybook main branch docs, commit e4ec607).
Confirmed: prefix and access forms per builder, `.env` files, head/body substitution, secrets warning, build-time hardcoding, `env` config field.
Method: documentation only; no commands were run.
