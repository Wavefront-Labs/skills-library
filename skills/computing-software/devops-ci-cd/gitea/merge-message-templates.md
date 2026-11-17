---
id: computing-software.devops-ci-cd.gitea.merge-message-templates
name: merge-message-templates
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-merge-template, gitea, default-merge-message, squash-template, rebase-template, closing-issues-variable, reviewed-on-trailer]
level: practitioner
status: docs-checked
description: "Customise Gitea default merge commit messages with .gitea/default_merge_message template files per merge style and the available ${...} variables."
sources: ["https://docs.gitea.com/usage/issues-prs/merge-message-templates/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea merge message templates

Place Markdown files in `.gitea/default_merge_message/`:
- `DEFAULT_TEMPLATE.md`: used for any merge style without its own template
- `MERGE_TEMPLATE.md`
- `REBASE_TEMPLATE.md`
- `REBASE-MERGE_TEMPLATE.md`
- `SQUASH_TEMPLATE.md`
- `MANUALLY-MERGED_TEMPLATE.md`
- `REBASE-UPDATE-ONLY_TEMPLATE.md`

Variables are written `${Name}` and follow Go `os.Expand` syntax:
- Repositories and branches: `BaseRepoOwnerName`, `BaseRepoName`, `BaseBranch`, `HeadRepoOwnerName`, `HeadRepoName`, `HeadBranch`
- Pull request: `PullRequestTitle`, `PullRequestDescription`, `PullRequestPosterName`, `PullRequestIndex`, `PullRequestReference` (e.g. `#1`, `!2`)
- `ClosingIssues`: all issues the PR will close, e.g. `close #1, close #2`
- `ReviewedOn`: e.g. `Reviewed-on: https://gitea.com/foo/bar/pulls/1`
- `ReviewedBy`: approver, e.g. `Reviewed-by: Jane Doe <jane.doe@example.com>`

## Rebase
When rebasing without a merge commit, `REBASE_TEMPLATE.md` rewrites the message of the last commit, and also gets `CommitTitle` and `CommitBody`.

Choosing a file: put shared wording in `DEFAULT_TEMPLATE.md` and add a per-style file only where a style needs different text, since a style without its own file falls back to the default.
Example `SQUASH_TEMPLATE.md` using only documented variables:
```
${PullRequestTitle} (${PullRequestReference})

${PullRequestDescription}

${ClosingIssues}
${ReviewedOn}
${ReviewedBy}
```

## Checked

2026-11-03: read https://docs.gitea.com/usage/issues-prs/merge-message-templates/ line by line; the commands, options, defaults and values stated above match those pages.
Changed: Removed the unconfirmed claim that trailer lines are the documented way to record review links.
Method: documentation only; no commands were run.
