---
id: computing-software.devops-ci-cd.gitea.code-owners
name: code-owners
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-codeowners, gitea, codeowners-regexp, negative-code-owner-rule, required-code-owner-approval, team-code-owner]
level: practitioner
status: docs-checked
description: "Write a Gitea CODEOWNERS file with Go regexp rules, negative patterns and escaping, and enforce owner approval through branch protection."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/repository/code-owners.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea CODEOWNERS

Gitea looks for the file in this order and uses the first found: `./CODEOWNERS`, `./docs/CODEOWNERS`, `./.gitea/CODEOWNERS`.

## Format
`<regexp rule> <@user or @org/team> [@user or @org/team]...` with **Go regular expressions**, not gitignore globs. A rule starting with `!` is negative: it matches every file except the one given. Owners of every rule matching a changed file are automatically requested to review the pull request. `#` starts a comment.
```bash
.*\\.go @user1 @user2 # comment
frontend/src/.*\\.js @org1/team1 @org1/team2 @user3
!frontend/src/.* @org1/team3 @user5
docs/(aws|google|azure)/[^/]*\\.(md|txt) @user8 @org1/team4
!/assets/.*\\.(bin|exe|msi) @user9
```

## Escaping
Escape `#`, space and `\` with a single `\` in the path part: `dir/with\#hashtag @user1`, `path\ with\ space @user2`, `path/with\\backslash @user3`. Regexp metacharacters (`.+*?()|[]{}^$\`) need `\\`: `path/\\.with\\.dots`, `path/with\\+plus`.

## Enforcing approval
In a protected branch rule (see `gitea-branch-protection`), enable code owner approval of modified files. The PR is then blocked until at least one owner of every applicable rule has approved. Example file `.*\\.go @Bob`, `.*\\.md @Sally @Chris`, `migrations/.* @Alice`: a `.go` change needs Bob; a `.md` change needs Sally or Chris; a `migrations` change needs Alice. Rules are composable: a PR touching `.go` and `.md` needs Bob plus one of Sally or Chris.

## Checked
2026-11-03. File lookup order, format, negative rules, escaping and approval enforcement confirmed against the Gitea docs page code-owners.md (raw markdown, gitea/docs main branch). Removed the claim that forgetting to escape is the usual cause of over-matching.
Method: documentation only; no commands were run.
