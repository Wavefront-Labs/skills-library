---
id: computing-software.devops-ci-cd.turborepo.turbo-json-env-key-wildcards-and-negation
name: turbo-json-env-key-wildcards-and-negation
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, env-key, wildcards, negation, env-patterns, task-scoped-env, framework-env, pattern-escaping]
level: practitioner
status: docs-checked
description: "Pattern rules for env arrays: trailing wildcards, leading ! negation, and escaping with backslashes for literal asterisks and exclamation marks."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`env` lists the environment variables a task depends on. Scope by task name or by `package#task`:

```json
{ "tasks": { "build": { "env": ["DATABASE_URL"] }, "web#build": { "env": ["API_SERVICE_KEY"] } } }
```

`build` impacts the hash of all build tasks; `web#build` only web's build. Framework Inference adds common prefixes such as `NEXT_PUBLIC_` automatically.

**Wildcards:** `"env": ["MY_API_*"]` includes every variable starting with `MY_API_`.
**Negation:** a leading `!` negates the whole pattern: `"env": ["!MY_API_URL"]` ignores that variable.

Pattern table from the docs:
- `"*"` matches every variable; `"!*"` excludes every variable.
- `"FOO*"` matches `FOO`, `FOOD`, `FOO_FIGHTERS`; `"FOO\*"` resolves to `"FOO*"` and does the same.
- `"FOO\\*"` matches a single variable named `FOO*`.
- `"!FOO*"` excludes all variables starting with `FOO`.
- `"\!FOO"` resolves to `"!FOO"` and excludes a single variable named `!FOO`; `"\\!FOO"` matches a variable named `!FOO`.
- `"FOO!"` matches a single variable named `FOO!`.

The same syntax applies to `globalEnv`. `passThroughEnv` is an allowlist made available to a task's runtime even in Strict Mode.

## Checked

2026-11-04. Read the `env`, Wildcards, Negation and Examples sections of the configuration reference, plus `globalEnv` and `passThroughEnv`; every pattern row matches. Removed the invented Verify step.

Method: documentation only; no commands were run.
