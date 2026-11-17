---
id: computing-software.web-development.biome.vcs-integration-and-gitignore
name: vcs-integration-and-gitignore
category: computing-software
field: web-development
product: biome
tags: [biome, vcs, git, gitignore, useignorefile, clientkind, git-info-exclude, worktrees, ignore-file]
level: practitioner
status: docs-checked
description: "Enable Biome's opt-in Git integration so it respects .gitignore, .ignore and .git/info/exclude via vcs.useIgnoreFile."
sources:
  - https://raw.githubusercontent.com/biomejs/website/main/src/content/docs/en/configuration/integrate-with-vcs.mdx
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
VCS integration is opt-in and only supports Git at the moment. It exists to take advantage of additional features that only a VCS can provide. You must enable `vcs.enabled` and set `vcs.clientKind` in the Biome configuration file. This configuration does nothing per se; you opt in to the features you want.

```json
{ "vcs": { "enabled": true, "clientKind": "git" } }
```

## Use the ignore file

Enable `vcs.useIgnoreFile` to make Biome ignore all files and directories listed in the project's VCS ignore files, as well as `.ignore` files. For Git repositories, Biome reads `.gitignore` files and Git's local exclude file at `.git/info/exclude`. In linked worktrees, `.git/info/exclude` is read from the common Git directory, matching Git's own behaviour.

```json
{ "vcs": { "enabled": true, "clientKind": "git", "useIgnoreFile": true } }
```

Processing only changed or staged files is a separate opt-in feature (see the changed-since skill).

## Checked

2026-11-08. Read the cited page in full (raw mdx). Unchanged: opt-in, Git-only, the two required fields, the useIgnoreFile description and the worktree note. Removed as unsupported by this page: the claim that ESLint, Prettier and Stylelint skip .gitignore by default, the statement about protected lockfiles, the files.includes advice and the invented Verify step.

Method: documentation only; no commands were run.
