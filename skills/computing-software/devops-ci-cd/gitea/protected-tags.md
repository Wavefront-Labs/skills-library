---
id: computing-software.devops-ci-cd.gitea.protected-tags
name: protected-tags
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-protected-tags, gitea, tag-protection, tag-glob-pattern, tag-regex-pattern, release-tag-allowlist]
level: practitioner
status: docs-checked
description: "Restrict who may create or update Git tags in Gitea with glob or slash-wrapped regex patterns and user or team allowlists, with pattern examples."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/access-control/protected-tags.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea protected tags

Settings, **Tags**: enter a pattern, choose allowed users and/or teams, **Save**. **Leaving both allowlists empty means nobody can create or modify matching tags.**

The pattern is either a single name, a gobwas glob, or a regular expression **enclosed in slashes**.

| Kind | Pattern | Matches |
| --- | --- | --- |
| Glob | `v*` | `v`, `v-1`, `version2` |
| Glob | `v[0-9]` | `v0` to `v9` |
| Glob | `*-release` | `2.1-release`, `final-release` |
| Glob | `{v,rel}-*` | `v-1`, `rel-x` |
| Glob | `*` | every tag |
| Regex | `/\Av\d+\.\d+\.\d+\z/` | `v1.0.17`, `v2.1.0` |
| Regex | `/\Av\d+(\.\d+){0,2}\z/` | `v1`, `v2.1`, `v1.2.34` |
| Regex | `/\A(v\|rel)-/` | `v-`, `rel-x` |
| Regex | `/gitea/` | any name containing `gitea` |
| Regex | `/\Agitea\z/` | exactly `gitea` |

Anchoring matters for regexes: `/gitea/` matches anywhere, `/\Agitea\z/` only the whole name. A plain glob `gitea` matches only that tag. Use semantic-version regexes to guard release tags while leaving experimental tags free, and combine with a release workflow that runs as an allowlisted user.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
