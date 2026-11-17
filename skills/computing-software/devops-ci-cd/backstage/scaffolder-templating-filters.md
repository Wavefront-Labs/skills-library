---
id: computing-software.devops-ci-cd.backstage.scaffolder-templating-filters
name: scaffolder-templating-filters
category: computing-software
field: devops-ci-cd
product: backstage
tags: [nunjucks, parse-repo-url, template-filters, backstage]
level: advanced
status: docs-checked
description: "Transform values in templates with built-in filters such as parseRepoUrl and parseEntityRef, and register custom ones."
sources:
  - https://backstage.io/docs/features/software-templates/templating-extensions
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

Backstage templating uses Nunjitsu, a secure template engine supporting a focused subset of Nunjucks syntax. Check its compatibility guide when borrowing Nunjucks examples.

Filters transform values with the pipe syntax. Built-in ones include:

- `parseRepoUrl`, which splits a repository URL such as `github.com?repo=backstage&owner=backstage` into a RepoSpec with `owner`, `repo` and related parts.
- `parseEntityRef`, which extracts `kind`, `namespace` and `name` from an entity reference, optionally with a context supplying defaults.
- Further filters such as `pick` and `projectSlug` are listed in the docs.

```yaml
- id: log
  name: Parse Repo URL
  action: debug:log
  input:
    message: ${{ parameters.repoUrl | parseRepoUrl }}

- id: owner
  action: debug:log
  input:
    message: ${{ parameters.repoUrl | parseRepoUrl | pick('owner') }}
```

You can also register custom filters and global functions through the scaffolder extension point in a backend module, so organisation conventions such as a naming scheme live in code, not copy-pasted expressions.

`debug:log` is used in the docs examples to print what a filter returns.

## Checked

2026-11-03. Confirmed against the Backstage Templating Extensions page: Nunjitsu, `parseRepoUrl`, `parseEntityRef` (with `defaultKind`/`defaultNamespace`), `pick`, `projectSlug`, `scaffolderTemplatingExtensionPoint`. Removed: the property-access form `(x | parseRepoUrl).owner` (replaced by `pick('owner')`) and the claim about unrun steps.

Method: documentation only; no commands were run.
