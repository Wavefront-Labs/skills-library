---
id: computing-software.devops-ci-cd.turborepo.env-files-hashing-with-inputs-and-globaldependencies
name: env-files-hashing-with-inputs-and-globaldependencies
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, env-files, dotenv, globaldependencies, inputs, turbo-default, multiple-env-files, nextjs-env-files]
level: practitioner
status: docs-checked
description: "Turborepo does not load .env files; list them in inputs or globalDependencies so changes to values miss cache, with wildcard and framework examples."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/using-environment-variables.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`.env` files help locally, but **Turborepo does not load `.env` files into a task's runtime**. Your framework or a tool like `dotenv` does that. However, `turbo` must know when values change so they affect hashing: if you change a variable in your `.env` between builds, `build` should miss cache.

Add the files to the `inputs` key, or `globalDependencies` for all tasks:

```json
{
  "globalDependencies": [".env"],
  "tasks": { "build": { "inputs": ["$TURBO_DEFAULT$", ".env"] } }
}
```

`globalDependencies` affects all task hashes; `inputs` only the `build` hash. Capture several files with a wildcard: `".env*"`.

Note: `.env` files can load variables into the runtime even when those variables are not in `env`. Add your variables to `env` for CI and production builds.

**Next.js example** (`build` and `dev` differ): `build` has `env: ["MY_API_URL", "MY_API_KEY"]` and inputs `$TURBO_DEFAULT$`, `.env.production.local`, `.env.local`, `.env.production`, `.env`; `dev` has inputs `$TURBO_DEFAULT$`, `.env.development.local`, `.env.local`, `.env.development`, `.env`; `test` is `{}` since it uses no environment variables (your test task may still need `env`). The Vite example has the same shape.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/using-environment-variables); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
