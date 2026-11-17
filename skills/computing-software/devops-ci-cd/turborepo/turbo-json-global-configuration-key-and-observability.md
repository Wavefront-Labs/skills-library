---
id: computing-software.devops-ci-cd.turborepo.turbo-json-global-configuration-key-and-observability
name: turbo-json-global-configuration-key-and-observability
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, globalconfiguration, global-key, global-inputs, experimentalobservability, otel, package-tags, renamed-keys]
level: advanced
status: docs-checked
description: "Opt in to the global key that namespaces global settings, with renames and the changed semantics of global.inputs; plus experimentalObservability and package tags."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**`globalConfiguration`** future flag moves global keys under a top-level `global` key. Renames:
- `globalDependencies` to `global.inputs`
- `globalEnv` to `global.env`
- `globalPassThroughEnv` to `global.passThroughEnv`
- `ui`, `envMode`, `cacheDir`, `cacheMaxAge`, `cacheMaxSize`, `concurrency`, `daemon`, `noUpdateNotifier`, `dangerouslyDisablePackageManagerCheck`, `remoteCache`, `experimentalObservability` each move to `global.<same name>`.

Using any old top-level key while the flag is on produces a **hard error with a rename hint**.

```json
{
  "futureFlags": { "globalConfiguration": true },
  "global": { "inputs": ["tsconfig.json", ".env"], "env": ["NODE_ENV"], "passThroughEnv": ["AWS_SECRET_KEY"], "ui": "tui", "envMode": "strict" }
}
```

**Semantics change:** `global.inputs` files are prepended to every task's `inputs` for per-task hashing instead of contributing to the global hash. That lets individual tasks exclude specific global files with negation globs.

**`experimentalObservability`** (future flag, default `false`): honours the `experimentalObservability.otel` block to send run summaries to an OpenTelemetry Protocol (OTLP) collector.

**Package `tags`** (experimental): `"tags": ["utils"]` in a package `turbo.json` adds arbitrary string labels. They need not be registered in `boundaries.tags` and can be used with Boundaries. Root `turbo.json` tags label only the root package. Package tags are separate from task tags.

## Checked

2026-11-04. Read the `globalConfiguration`, `experimentalObservability`, `tags` and `global` entries of the configuration reference in full; the rename table, the hard-error statement, the semantics callout, the example and the tag rules match. Removed the invented Verify step.

Method: documentation only; no commands were run.
