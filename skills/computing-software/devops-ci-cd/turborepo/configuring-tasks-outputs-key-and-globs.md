---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-outputs-key-and-globs
name: configuring-tasks-outputs-key-and-globs
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, outputs, cache-outputs, glob-patterns, nextjs-outputs, vite-dist, tsc-dist, negated-globs]
level: practitioner
status: docs-checked
description: "Without outputs Turborepo restores no files from cache; declare outputs relative to the package for Next.js, Vite and tsc with negation globs."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
The `outputs` key tells Turborepo which **files and directories** to cache when a task completes successfully. **Without it, Turborepo caches no files, and a cache hit on later runs does not restore any file outputs.**

Examples for common tools:

```json
// Next.js
{ "tasks": { "build": { "outputs": [".next/**", "!.next/cache/**", "!.next/dev/**"] } } }
// Vite
{ "tasks": { "build": { "outputs": ["dist/**"] } } }
// tsc
{ "tasks": { "build": { "outputs": ["dist/**"] } } }
```

(The three are alternatives, not one file.) Globs are relative to the package, so `dist/**` handles the `dist` that each package outputs. A leading `!` negates a glob (the Next.js example uses it for `.next/cache` and `.next/dev`). For more on glob patterns, the docs point to the globbing specification (reference/globs).

Related guidance from the Caching guide: if you do not declare file outputs, Turborepo does not cache them. That may be fine for linters but not for tasks that produce files; if files are missing after a cache hit, make sure the task has `outputs`.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the unsupported reason given for the Next.js negation globs.

Method: documentation only; no commands were run.
