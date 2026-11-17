---
id: computing-software.devops-ci-cd.backstage.scaffolder-publish-defaults
name: scaffolder-publish-defaults
category: computing-software
field: devops-ci-cd
product: backstage
tags: [scaffolder-config, default-author, repo-visibility, backstage]
level: practitioner
status: docs-checked
description: "Set the default commit author and message for template publishing and control repository visibility."
sources:
  - https://backstage.io/docs/features/software-templates/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Templates create source code, so the Backstage app needs `integrations` configured for the provider hosting the repositories. After that, adjust publishing behaviour in `app-config.yaml`:

```yaml
scaffolder:
  defaultAuthor:
    name: Platform Bot # defaults to `Scaffolder`
    email: platform@example.com # defaults to `scaffolder@backstage.io`
  defaultCommitMessage: 'Initial scaffold' # defaults to 'Initial commit'
```

Control who can see a new repository with `repoVisibility` in the publish step:

```yaml
- id: publish
  name: Publish
  action: publish:github
  input:
    repoUrl: ${{ parameters.repoUrl }}
    repoVisibility: private # or `public`, `internal`
```

Notes:

- The author and message defaults apply to the initial commit created by publish actions.
- `repoUrl` values come from `RepoUrlPicker`, and `allowedHosts` limits which hosts users can pick.

## Checked

2026-11-03. Confirmed against the Backstage scaffolder Configuration page: `defaultAuthor` and `defaultCommitMessage` defaults, `repoVisibility` values, and the `allowedHosts`/integrations relationship from the Writing Templates page. Removed: advice about private defaults, token scopes and GitHub App rotation.

Method: documentation only; no commands were run.
