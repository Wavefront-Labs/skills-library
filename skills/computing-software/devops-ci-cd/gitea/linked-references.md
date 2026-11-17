---
id: computing-software.devops-ci-cd.gitea.linked-references
name: linked-references
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-closing-keywords, gitea, issue-references, mention-notification, time-tracking-commit, external-tracker-references, bang-pull-reference]
level: practitioner
status: docs-checked
description: "How Gitea parses mentions, issue and pull request references, closing and reopening keywords, spent-time syntax in commit messages, and external tracker reference rules."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/issues-prs/linked-references.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea linked references

Issue, PR and comment text, plus commit messages, are parsed for references. Ignored inside code text, and they need clear surrounding text such as spaces.

## Links
- `@username`, team or organization: mention link and possibly a notification (needs access to the content). Teams get mail notifications, whole organizations do not; commit messages never notify.
- Commit: SHA1 or a prefix of at least seven characters.
- `#1234`: issue or PR in the same repository, which also posts a notice in the target if the author can read it. `owner/repository#1234` for other repos. `!1234` makes a pull request link, which matters with an external tracker, where `#1234` is an external issue.

## Closing and reopening
A keyword before the reference closes or reopens the issue. Defaults: close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved; reopen, reopens, reopened. Administrators can customise the list in the config cheat sheet.
Accepted when at least one holds: the commenter can close/reopen at that moment, the reference is in a commit message, or it is in the PR description. In the PR-description case the issue changes only if the merger has the permission. Only PRs and commits trigger actions, and only issues are affected. A notice on the issue says it will close on merge.

## Spent time
After the issue number add `@<number><unit>`; units `m`, `h`, `d` (8 hours), `w` (5 days), `mo` (4 weeks); decimals and combinations are fine (`@1.5h`, `@1h10m`). Example commit message: `Fixed #123 spent @1h, refs #102, fixes #124 @1.5h` adds 1 hour to #123 and 1.5 hours to #124.

## External trackers
With an external tracker, `#1234` links to the external issue and `!1234` to a Gitea PR. In that repo the squash-merge commit message uses `!` by default. Alphanumeric IDs such as `AAA-1234` link to the external issue for the current repository only. References between repositories with different tracker types are not fully supported and may render invalid links.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
