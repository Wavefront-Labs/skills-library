---
id: computing-software.devops-ci-cd.turborepo.ci-run-tasks-filter-and-docker-prune
name: ci-run-tasks-filter-and-docker-prune
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, ci, filter, shallow-clone, git-history, docker, turbo-prune, global-turbo]
level: practitioner
status: docs-checked
description: "Run the same registered tasks in CI, filter by package, directory or Git history (not possible with shallow clones), and use turbo prune for lean Docker images."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
By installing `turbo` globally on development and CI machines you get one mental model from development to shipping: tasks registered in `turbo.json` work exactly the same in CI.

**Filtering for entry points.** `--filter` works in CI exactly as locally: by package, directory and Git history.

Caveat: filtering by source control changes is only possible when history is available on the machine. **Shallow clones do not have history**, so these filters cannot work there.

The `--affected` flag runs tasks only in packages with changes (see the affected skill).

**Docker.** Docker is part of many deployment pipelines. The `prune` subcommand helps ship lightweight images by removing unnecessary dependencies and code. See the dedicated Docker guide for deploying from a Turborepo.

Related reading from the guide: Configuring Tasks for how to set up tasks, and the CI guides for vendor-specific examples.

With shallow clones, `--affected` handles them more gracefully than bespoke filtering because it falls back to running all tasks.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: an unsourced filter-range rule and a Verify step using git log.

Method: documentation only; no commands were run.
