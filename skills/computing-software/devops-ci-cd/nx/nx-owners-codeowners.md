---
id: computing-software.devops-ci-cd.nx.nx-owners-codeowners
name: nx-owners-codeowners
category: computing-software
field: devops-ci-cd
product: nx
tags: [nx, owners, codeowners, enterprise, github, gitlab, bitbucket]
level: practitioner
status: docs-checked
description: "Define project-level code ownership with @nx/owners (Enterprise) in nx.json or project.json and let a sync generator write CODEOWNERS for GitHub, GitLab or Bitbucket."
sources:
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/owners.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/activate-license.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/enterprise/conformance.mdoc
  - https://raw.githubusercontent.com/nrwl/nx/master/astro-docs/src/content/docs/reference/nx-json.mdoc
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: declare owners per project and generate a valid CODEOWNERS file instead of hand-maintaining folder paths.

Prereqs: Nx Enterprise license (`nx register <key>` or `NX_KEY`, see nx-conformance-rules) and the plugin from the Owners overview page (`@nx/owners`).

Workspace patterns in `nx.json`:
```json
{ "owners": {
  "format": "github",
  "patterns": [
    { "description": "Joe's Rust projects", "projects": ["tag:rust"], "owners": ["@joelovesrust"] },
    { "description": "Finance projects", "projects": ["finance-*"], "owners": ["@finance-team"] },
    { "description": "Alphabet soup", "projects": ["admin", "books", "cart"], "owners": ["@alice", "@bob"] },
    { "description": "CI Workflows", "files": [".github/workflows/**/*"], "owners": ["@devops"] }
  ] } }
```
- `format`: `github`, `bitbucket` or `gitlab`.
- Each pattern uses `projects` (names, globs, `tag:` references) or `files` (globs), plus `owners`.

Per project in `project.json`, a map of glob to owners:
```json
{ "owners": { "**/*": ["@ahmed", "@petra"], "package.json": ["@ahmed"] } }
```

Output: a sync generator compiles these into the platform file (e.g. `.github/CODEOWNERS`), turning each project into its path:
```
# Finance projects
/packages/finance-ui @finance-team
/packages/my-project/ @ahmed @petra
/packages/my-project/package.json @ahmed
```
Because it is a sync generator, `nx sync` (which runs all sync generators) regenerates it (nx-sync-generators).

The Conformance page's sample config includes the rule `@nx/conformance/ensure-owners` (nx-conformance-rules).

## Checked

2026-11-07. Confirmed: the owners configuration, generated CODEOWNERS and nx register / NX_KEY against the Owners and Activate license pages. Removed: nx sync:check (not on any page read), the claim that ensure-owners requires every project to have an owner (the page only lists the rule), and an invented Verify step.

Method: documentation only; no commands were run.
