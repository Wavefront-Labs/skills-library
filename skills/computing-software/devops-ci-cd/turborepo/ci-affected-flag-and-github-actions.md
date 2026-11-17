---
id: computing-software.devops-ci-cd.turborepo.ci-affected-flag-and-github-actions
name: ci-affected-flag-and-github-actions
category: computing-software
field: devops-ci-cd
product: turborepo
tags: [turborepo, affected, ci, github-actions, github-base-ref, github-event-path, shallow-clone, remote-cache]
level: practitioner
status: docs-checked
description: "Use turbo run --affected to execute tasks only in changed packages, and how it infers the base in GitHub Actions pull requests and pushes."
sources:
  - https://raw.githubusercontent.com/vercel/turborepo/main/apps/docs/content/docs/crafting-your-repository/constructing-ci.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
`turbo run build --affected` runs tasks only in packages that have changes.

**Use it when**
- you run many tasks across packages and only want those in packages with code changes;
- you are not using a Remote Cache but still want minimal work in CI;
- you use a Remote Cache in a large repository: fewer tasks restored from cache means less data across the network and faster restoration;
- you already use advanced filtering to build similar behaviour: `--affected` can simplify scripts and handles shallow clones more gracefully than bespoke filtering, because it falls back to running all tasks.

**In GitHub Actions** Turborepo detects the environment by inspecting variables such as `GITHUB_BASE_REF`. In a PR it compares the base branch with the head branch to find affected packages.
- `GITHUB_BASE_REF` works for `pull_request` and `pull_request_target` events but is unavailable on regular push events.
- For pushes it uses `GITHUB_EVENT_PATH` to determine the base branch.
- For force pushes and for pushing a branch with no additional commits, it compares to the parent of the first commit on the branch.

## Checked

2026-11-04. Read in full from the vercel/turborepo docs source (apps/docs/content/docs/: crafting-your-repository/constructing-ci); commands, flags, key names, defaults and example values were matched against it. Removed: a misplaced cross-reference to task-level inputs and the Verify step.

Method: documentation only; no commands were run.
