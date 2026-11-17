---
id: computing-software.devops-ci-cd.turborepo.turbo-json-inputs-reference-turbo-root-and-deferred-hashing
name: turbo-json-inputs-reference-turbo-root-and-deferred-hashing
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, inputs-reference, turbo-root, turbo-default, deferred-hashing, jit-mode, dependencyoutputs, dry-run-json, always-inputs]
level: advanced
status: docs-checked
description: "Reference for inputs: files always hashed, $TURBO_DEFAULT$ and $TURBO_ROOT$, and the jit and dependencyOutputs modes with their constraints."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/reference/configuration.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`inputs` defaults to `[]`, meaning all files in the package that are checked into source control. Globs are relative to the package's `package.json`. These are **always** inputs, even if you try to ignore them: `package.json`, `turbo.json` and package manager lockfiles.

Specifying `inputs` opts out of the default behaviour of considering `.gitignore`; reconstruct the globs or use `$TURBO_DEFAULT$`:

```json
{ "tasks": { "check-types": { "inputs": ["$TURBO_DEFAULT$", "!README.md"] } } }
```

**`$TURBO_ROOT$`.** For files outside the package, start a glob with `$TURBO_ROOT$` to make it relative to the repository root: `"inputs": ["$TURBO_ROOT$/tsconfig.json", "src/**/*.ts"]`. The same prefix applies to `outputs` that must be relative to the root; output paths must resolve inside the repository root or Turborepo will not cache them.

**Deferred hashing.** Structured entries defer hashing until dependencies finish; tasks depending on a deferred task are deferred too.
- `mode: "jit"` hashes the files matching `globs` just before execution. Example: `build` depends on `codegen` (`cache: false`) and has inputs `["$TURBO_DEFAULT$", "!src/generated/**", { "mode": "jit", "globs": ["src/generated/**"] }]`.
- `mode: "dependencyOutputs"` hashes the intersection of a dependency's declared `outputs` and `globs`, e.g. `{ "mode": "dependencyOutputs", "globs": ["dist/**/*.d.ts"], "from": ["^check-types"] }`. It creates no graph edges; selected tasks must already be present through `dependsOn`.

Rules: `from` is valid only with `dependencyOutputs`; it defaults to the task's direct task dependencies; a selected `dependencyOutputs` task must declare `outputs`. Because final cache keys are unknown until execution, `--dry=json` reports `hash: null` and a `hashReason`.

Outputs note: omitting `outputs` or passing `[]` caches nothing except logs, which are always cached when caching is enabled.

## Checked

2026-11-04. Read the `inputs`, `$TURBO_DEFAULT$`, `$TURBO_ROOT$`, Deferred hashing and `outputs` entries of the configuration reference in full; defaults, rules and examples match. Removed the invented Verify step.

Method: documentation only; no commands were run.
