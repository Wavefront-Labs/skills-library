---
id: computing-software.devops-ci-cd.rundeck.git-scm-shared-repository
name: git-scm-shared-repository
category: computing-software
field: devops-ci-cd
product: rundeck
tags: [rundeck, scm-git, shared-repository, file-path-template, import-regex]
level: advanced
status: docs-checked
description: "Share one Git repository and branch between several Rundeck projects using per-project folders in the file path template and regex-filtered imports."
sources:
  - https://raw.githubusercontent.com/rundeck/docs/4.0.x/docs/manual/projects/scm/git.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Two ways to share a repository across projects: use a different branch per project, or the same branch with a folder per project. The folder method from the docs:

Export, in project-a:
- **Export UUID Behavior**: `original`
- **File Path Template**: `project-a/${job.group}${job.name}-${job.sourceId}.${config.format}`

In project-b use the same settings but start the template with `project-b/`.

Import into a project that consumes project-a's jobs:
- **Import UUID Behavior**: `archive`
- **File Path Template**: `project-a/${job.group}${job.name}-${job.sourceId}.${config.format}`
- **Match a Regular Expression?**: `yes`, with expression `project-a/.*\.xml` (or `.yaml` or `.json` to match your format)

Do likewise with `project-b/` for the other project.

Gotchas:
- `${job.sourceId}` is a random UUID different from `${job.id}`; `original` export and `archive` import make the two sides agree on it.
- The docs do not recommend using the same repository and branch for both export and import plugins in one project.
- The page's final example regex for project-b contains a `project-a/` typo for json; use `project-b/.*\.json`.

## Checked

2026-11-04. Confirmed against the Rundeck docs page Git Plugin, section Use the same repo for multiple projects: per-project folder templates, original export and archive import UUID behaviours, regex values, the not-recommended same repo and branch note, and the project-a typo in the project-b json regex. Nothing removed.

Method: documentation only; no commands were run.
