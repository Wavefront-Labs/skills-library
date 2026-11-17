---
id: computing-software.web-development.bun.add-git-tarball-local
name: add-git-tarball-local
category: computing-software
field: web-development
product: bun
tags: [git-dependency, tarball-dependency, local-path-dependency, ssh-git]
level: advanced
status: docs-checked
description: "Add dependencies from git repositories, tarball URLs and local paths with bun add, including SSH behaviour, credentials in URLs and prepare-script limits."
sources:
  - https://raw.githubusercontent.com/oven-sh/bun/main/docs/pm/cli/add.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
```bash
bun add git@github.com:moment/moment.git
bun add zod@https://registry.npmjs.org/zod/-/zod-3.21.4.tgz
bun add ../shared/logger        # folder or local .tgz
```

Git (protocols `github:`, `git`, `git+ssh`, `git+https`):
- Needs git 2.24 or newer, run with the environment `bun` started in; `.env` values like `PATH` or `GIT_SSH_COMMAND` do not reach it.
- Bun tries an SSH URL over HTTPS first, then over SSH, and sets `GIT_SSH_COMMAND` to `ssh -oStrictHostKeyChecking=accept-new` unless you define your own SSH command.
- A committed `node_modules` is deleted unless `package.json` has `bundleDependencies`.
- `prepare` runs only if the package is in `trustedDependencies`, and devDependencies are not installed first, so build tools may be missing.

Tarball: credentials in the URL become an `Authorization: Basic` header, but the URL with credentials is still saved to `package.json` and the lockfile. Percent-encode special characters (`p@ss` becomes `p%40ss`).

Local path: written relative to the target `package.json`; with `--global` it is absolute.

## Checked

2026-11-04. Confirmed against bun docs pm/cli/add.mdx: git protocols, git 2.24, environment, SSH fallback, node_modules deletion, prepare and trustedDependencies, tarball credentials, local paths. Reworded the SSH-over-HTTPS order.

Method: documentation only; no commands were run.
