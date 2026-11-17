---
id: computing-software.devops-ci-cd.gitea.agit-flow
name: agit-flow
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-agit-flow, gitea, refs-for, topic-branch, pr-without-fork, push-force-option]
level: practitioner
status: docs-checked
description: "Open Gitea pull requests by pushing to refs/for/<branch> with topic, title, description and force-push options, without a fork or write access."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/issues-prs/agit.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# AGit flow in Gitea

Since Gitea 1.13, AGit lets a user create a pull request straight from a push, with no fork and no write access to the repository. The server needs Git 2.29 or higher.

## Command
```shell
git push origin HEAD:refs/for/main -o topic="topic_of_my_PR"
```
General form: `git push <remote> <local-rev>:refs/for/<branch>[/<topic>] [-o <option>[=<value>] ...]`
- `<remote>` must point at the target repository itself, not a fork.
- `<local-rev>` is the local branch or commit holding the proposed changes.
- `refs/for/<branch>` creates a normal PR into `<branch>`. It is the only prefix supported; `refs/draft/...` and `refs/for-review/...` are reserved and create nothing.
- The topic may be appended to the refspec instead of `-o topic`. Without a topic in either place the push is rejected with `topic-branch is not set`.

## Options
- `topic`: required to trigger a PR (unless in the refspec). It becomes the name of the branch that holds the changes under review, prefixed with your user name.
- `title`, `description`: optional but recommended; used only when the topic has no PR yet.
- `force-push=true`: force-update the target; `-o force-push` with no value works too.

Fuller example:
```shell
git push origin HEAD:refs/for/main -o topic="topic_of_my_PR" -o title="Title of the PR" -o description="# The PR Description\nThis can be **any** markdown content.\n- [x] Ok"
```
`title` and `description` are only used for topics that do not already have an associated PR.

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Removed the claim that pushing again with the same topic updates the PR (the page only says title and description are used for topics without a PR).
Method: documentation only; no commands were run.
