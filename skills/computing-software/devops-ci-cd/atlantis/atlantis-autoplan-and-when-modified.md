---
id: computing-software.devops-ci-cd.atlantis.atlantis-autoplan-and-when-modified
name: atlantis-autoplan-and-when-modified
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [autoplan, when-modified, autoplan-modules, modules, bitbucket]
level: practitioner
status: docs-checked
description: "Understand the autoplan algorithm, tune when_modified patterns, disable autoplan and plan module dependents."
sources: ["https://www.runatlantis.io/docs/autoplanning", "https://www.runatlantis.io/docs/repo-level-atlantis-yaml"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis autoplan and when modified

Atlantis autoplans on any new pull request or new commit to an existing one.

Algorithm:
1. List files modified in the PR.
2. Keep files matching `--autoplan-file-list` (default includes `.tf`, `.tf.json`, `.tfvars`, `.tofu`, `.tofu.json`).
3. Find the directories containing them.
4. If the path has no `modules/` segment, plan in that directory.
5. If it does, look one level above `modules/`; if that directory holds `*.tf`, `*.tf.json`, `*.tofu`, `*.tofu.json` or `terragrunt.hcl`, plan there, otherwise ignore the change.

So editing a shared top-level `modules/module1/main.tf` triggers no plan. Options: list projects in `atlantis.yaml`, enable `--autoplan-modules` (maps projects to their local module dependencies), or plan manually with `atlantis plan -d <dir>`.

Per project:

```yaml
autoplan:
  enabled: true
  when_modified: ["*.tf", "../modules/**/*.tf", ".terraform.lock.hcl"]
```

`when_modified` uses `.dockerignore`-style patterns relative to the project `dir`, applies to autoplans and manual plans, and replaces the defaults entirely (default: `**/*.tf*`, `**/*.tofu`, `**/*.tofu.json`, `**/terragrunt.hcl`, `**/.terraform.lock.hcl`). Set `enabled: false` to stop autoplanning a project.

Bitbucket has no webhook for only new PR or commit, so Atlantis caches the last commit; a cleared cache (restart, or several instances behind a load balancer) can cause extra plans.

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Autoplanning, Repo Level atlantis.yaml. Removed or fixed: nothing needed removing.

Method: documentation only; no commands were run.
