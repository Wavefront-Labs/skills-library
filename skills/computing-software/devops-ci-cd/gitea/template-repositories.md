---
id: computing-software.devops-ci-cd.gitea.template-repositories
name: template-repositories
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-template-repo, gitea, template-file-expand, template-variable-expansion, template-transformers, repo-name-pascal, gobwas-glob]
level: practitioner
status: docs-checked
description: "Make a Gitea template repository with a .gitea/template file listing globs to expand, [expand] and [exclude] sections, variables and case transformers."
sources: ["https://docs.gitea.com/usage/repository/template-repositories/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea template repositories

Available since Gitea 1.11. Creating a repo from a template copies most content and can inject variables. **Nothing is expanded by default**: only files matching a glob in `.gitea/template` are scanned, and that file itself is not copied into generated repositories. Globs are gobwas/glob, similar to `.gitignore` but not identical; paths are relative to the repo root.

```gitignore
**.go
text/*.txt
a/b/c/d.json
**.[bB][aA][tT]
```
Sections are also supported:
```
[expand]
*.md

[exclude]
*.log
```

## Variables
Use `$VAR` or `${VAR}`; escape with `$$VAR` or `$${VAR}`. File names and paths matching are expanded too, conservatively sanitised for cross-platform filesystems.
`YEAR`, `MONTH`, `MONTH_ENGLISH`, `DAY`; `REPO_NAME`, `REPO_DESCRIPTION`, `REPO_OWNER`, `REPO_LINK`, `REPO_HTTPS_URL`, `REPO_SSH_URL` and the matching `TEMPLATE_*` set (`TEMPLATE_NAME`, `TEMPLATE_DESCRIPTION`, `TEMPLATE_OWNER`, `TEMPLATE_LINK`, `TEMPLATE_HTTPS_URL`, `TEMPLATE_SSH_URL`).

## Transformers (1.12.0+)
Only `MONTH_ENGLISH`, `REPO_NAME`, `TEMPLATE_NAME`, `REPO_OWNER` and `TEMPLATE_OWNER` are transformable. Append the transformer: `${REPO_NAME_PASCAL}`. For input `go-sdk`: SNAKE `go_sdk`, KEBAB `go-sdk`, CAMEL `goSdk`, PASCAL `GoSdk`, LOWER `go-sdk`, UPPER `GO-SDK`, TITLE `Go-Sdk`.

## Checked

2026-11-03: read https://docs.gitea.com/usage/repository/template-repositories/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Removed the unconfirmed `repo.template` push-option sentence.
Method: documentation only; no commands were run.
