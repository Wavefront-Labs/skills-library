---
id: computing-software.web-development.mkdocs.gh-deploy-project-pages
name: gh-deploy-project-pages
category: computing-software
field: web-development
product: mkdocs
tags: [gh-deploy, github-pages, project-pages, remote-branch]
level: practitioner
status: docs-checked
description: "Publish docs to GitHub Project Pages with mkdocs gh-deploy, which builds and pushes the gh-pages branch; warns about uncommitted files and hand edits."
sources:
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/deploying-your-docs.md
  - https://raw.githubusercontent.com/mkdocs/mkdocs/master/docs/user-guide/configuration.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
From the primary branch of the source repository:

```sh
mkdocs gh-deploy
```

MkDocs builds the docs, uses the ghp-import tool to commit them to the `gh-pages` branch and pushes that branch. See `mkdocs gh-deploy --help` for options.

Config defaults: `remote_branch: gh-pages`, `remote_name: origin`; both can be overridden by command line options.

Warnings:
- You cannot review the built site before it is pushed. Check changes first with `mkdocs build` or `mkdocs serve`.
- Never hand-edit files in the pages branch: the next deploy overwrites them.
- Untracked files or uncommitted work in the local repository will be included in the deployed pages.

See `gh-deploy-user-org-pages`, `github-custom-domain`.

## Checked

2026-11-04. Confirmed against Deploying your docs (Project Pages) and the configuration guide (remote_branch, remote_name): `gh-pages` default, ghp-import, `--help`, and the three warnings. Removed: a generic verify line.

Method: documentation only; no commands were run.
