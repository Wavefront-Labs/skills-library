---
id: computing-software.devops-ci-cd.backstage.scaffolder-builtin-actions
name: scaffolder-builtin-actions
category: computing-software
field: devops-ci-cd
product: backstage
tags: [scaffolder-actions, action-modules, publish-actions, backstage]
level: practitioner
status: docs-checked
description: "Find and install the scaffolder action modules for fetching, publishing and registering across providers."
sources:
  - https://backstage.io/docs/features/software-templates/builtin-actions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The scaffolder ships core actions for fetching content (`fetch:plain`, `fetch:template`), registering entities (`catalog:register`) and creating and publishing git repositories, and adds provider actions through separate modules you install in the backend.

Documented action modules:

- Azure DevOps: `@backstage/plugin-scaffolder-backend-module-azure`
- Bitbucket Cloud and Bitbucket Server: `...-bitbucket-cloud`, `...-bitbucket-server`
- Gerrit and Gitea: `...-gerrit`, `...-gitea`
- GitHub: `@backstage/plugin-scaffolder-backend-module-github`
- GitLab: `@backstage/plugin-scaffolder-backend-module-gitlab`
- Rails, Yeoman, Sentry and Cookiecutter (`...-rails`, `...-yeoman`, `...-sentry`, `...-cookiecutter`)

```bash
yarn --cwd packages/backend add @backstage/plugin-scaffolder-backend-module-github
```

```ts
backend.add(import('@backstage/plugin-scaffolder-backend'));
backend.add(import('@backstage/plugin-scaffolder-backend-module-github'));
```

Publish actions such as `publish:github` create repositories; the hosts a template publishes to come from the `integrations` config in `app-config.yaml`.

All registered actions are listed at `/create/actions` (for local development `http://localhost:3000/create/actions`).

## Checked

2026-11-03. Confirmed against the Backstage Builtin actions page: module list and package names, install command, backend.add lines, `/create/actions`. Removed: the troubleshooting claim about unknown actions and the statement that the list shows schemas (not in the page).

Method: documentation only; no commands were run.
