---
id: computing-software.devops-ci-cd.atlantis.atlantis-autodiscovery-modes
name: atlantis-autodiscovery-modes
category: computing-software
field: devops-ci-cd
product: atlantis
tags: [autodiscovery, ignore-paths, monorepo, atlantis-yaml, dynamic-config]
level: advanced
status: docs-checked
description: "Choose between auto, enabled and disabled project autodiscovery and use ignore_paths for multi-instance monorepos."
sources: ["https://www.runatlantis.io/docs/repo-level-atlantis-yaml", "https://www.runatlantis.io/docs/server-side-repo-config"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Atlantis autodiscovery modes

`autodiscover` controls whether Atlantis finds projects not listed in `atlantis.yaml`.

- `auto` (default): discovers projects only when the repo has no `projects` configured.
- `disabled`: never discovers. Useful when pre-workflow hooks generate the config dynamically.
- `enabled`: discovers projects from modified files even when `projects` is set. Manually configured projects win on directory conflicts. The docs note that `enabled` is ignored if set on the server side.
- `ignore_paths`: a list of doublestar globs to skip.

`ignore_paths` applies to autoplan and `atlantis plan` without `-d`, to `atlantis apply` without `-d` when filtering pending plans, and to targeted `-d` commands (`plan`, `apply`, `import`, `state rm`) when autodiscovery is enabled and the path has no explicit project config. This lets several Atlantis instances manage different subtrees of one monorepo.

Server-side, `autodiscover` can be set per repo entry in `repos.yaml`; if any part is set there it replaces the entire repo-config autodiscover setting.

```yaml
version: 3
autodiscover:
  mode: enabled
  ignore_paths:
  - some/path
```

## Checked

2026-11-03. Prose and identifiers confirmed against the official Atlantis docs page(s): Repo Level atlantis.yaml (Autodiscovery Config), Server Side Repo Config. Removed or fixed: the closing Terraform Cloud workspace sentence (it belongs to the terraform-versions page and was not stated for autodiscovery).

Method: documentation only; no commands were run.
