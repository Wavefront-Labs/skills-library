---
id: computing-software.devops-ci-cd.turborepo.configuring-tasks-inputs-and-turbo-default
name: configuring-tasks-inputs-and-turbo-default
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, inputs, turbo-default, task-hash, cache-hit-ratio, gitignore, deferred-hashing, jit-mode, dependencyoutputs]
level: practitioner
status: docs-checked
description: "Narrow task hashes with inputs, restore the default set with $TURBO_DEFAULT$, and know the deferred hashing modes for files created by dependencies."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/configuring-tasks.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`inputs` lists the files included in a task's hash. By default Turborepo includes **all files in the package tracked by Git**. Narrow it for a task that depends on a subset of files:

```json
{ "tasks": { "spell-check": { "inputs": ["**/*.md", "**/*.mdx"] } } }
```

Now **only** Markdown changes miss the cache for `spell-check`.

**Warning:** setting `inputs` opts out of all default input behaviour including following source control. Your `.gitignore` is no longer respected, and you must make sure your globs do not capture ignored files.

**`$TURBO_DEFAULT$`** restores the defaults and lets you fine-tune them:

```json
{ "tasks": { "build": { "inputs": ["$TURBO_DEFAULT$", "!README.md"] } } }
```

The `build` task uses the default inputs but ignores changes to `README.md`, so a README edit still hits cache. Fine-tuning like this can raise cache hit ratios for files known not to affect output.

**Deferred hashing.** Some tasks need to hash files created by another task in the same run. Use structured `inputs` with `mode: "jit"` or `mode: "dependencyOutputs"` to defer hashing until the task's dependencies have completed. The full shape is in the configuration reference.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/configuring-tasks); commands, flags, key names, defaults and example values were matched against it. Removed: the Verify step the page does not support.

Method: documentation only; no commands were run.
