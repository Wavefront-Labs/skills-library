---
id: computing-software.software-engineering.git.server-side-hooks-and-branch-protection
name: server-side-hooks-and-branch-protection
category: computing-software
field: software-engineering
product: git
tags: [git, git-customization, server-side-hooks, pre-receive, update-hook, post-receive, branch-protection, rulesets, policy]
level: practitioner
status: docs-checked
description: "Enforce repository policy on the server with pre-receive/update hooks or forge branch protection and rulesets: required reviews, checks, signatures, no force-push."
sources:
  - https://git-scm.com/book/en/v2/Customizing-Git-An-Example-Git-Enforced-Policy
  - https://git-scm.com/docs/githooks
  - https://git-scm.com/docs/git-config
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  - https://docs.gitlab.com/ee/administration/server_hooks.html
  - https://github.com/integrations/terraform-provider-github/blob/main/docs/resources/repository_ruleset.md
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Server-side hooks and branch protection

**Goal:** rules that cannot be skipped with `--no-verify`: protected branches, required checks, commit policy.

## 1. Self-hosted Git: hooks in the bare repo
| Hook | Input | Effect of non-zero exit |
|---|---|---|
| `pre-receive` | stdin lines `<old> <new> <ref>` for the whole push | no refs are updated |
| `update` | args `<ref> <old> <new>`, once per ref | rejects that ref only |
| `post-receive` | stdin lines in the pre-receive format, for refs actually updated; runs once after all updates | cannot undo the push (notifications, CI triggers, deploy) |

Example `pre-receive` blocking deletion and non-fast-forward pushes of main:
```sh
#!/bin/sh
zero=0000000000000000000000000000000000000000
while read old new ref; do
  [ "$ref" = refs/heads/main ] || continue
  [ "$new" = "$zero" ] && { echo "deleting main is not allowed"; exit 1; }
  if [ "$old" != "$zero" ] && ! git merge-base --is-ancestor "$old" "$new"; then
    echo "non-fast-forward push to main rejected"; exit 1
  fi
done
```
New-branch pushes have `old` = all zeros (the all-zeroes object name), so there is no `$old..$new` range to walk for them.
Built-in alternatives: `receive.denyNonFastForwards=true`, `receive.denyDeletes=true`.

## 2. Forges: branch protection and rulesets
GitHub rulesets (or classic branch protection) on `main` and `release/*`:
- Require a pull request, N approvals, CODEOWNERS review, dismiss stale approvals on push.
- Require status checks to pass (pick the exact job names) and branch up to date.
- Require signed commits, linear history, block force pushes and deletion.
- Restrict who can push / bypass list; prefer no admin bypass.
GitLab: protected branches + push rules + server hooks (self-managed; the GitLab docs install them from a `custom_hooks` archive with `gitaly hooks set`).

## 3. Manage as code
```bash
gh api repos/org/repo/rulesets --method POST --input ruleset.json
```
Or Terraform `github_repository_ruleset`, so protection is reviewed and consistent across repos.

## Gotchas
- Hooks run before refs update and their output is forwarded to the pushing client, so keep `pre-receive` fast.
- GitHub rulesets have an "Evaluate" enforcement mode in which the ruleset is not enforced; check the GitHub docs for the plans that offer it before planning a rollout around it.
- Tag protection matters too: GitHub rulesets can target tags as well as branches, so block moving or deleting release tags.

## Verify
- Attempt `git push --force` to main and a direct push without a PR from a test account: both are rejected with the policy message.

## Checked

Checked 2026-10-25 against the git/git Documentation tree at master (latest commit 2026-10-22), the github/docs repository (main), the GitLab docs mirror (gitlabhq) and the Terraform GitHub provider docs. Confirmed: githooks `pre-receive` (stdin `<old-oid> <new-oid> <ref-name>`, all-zero old id for new refs, non-zero exit updates no refs), `update` (three arguments, per ref) and `post-receive`; `receive.denyNonFastForwards` and `receive.denyDeletes`; GitHub ruleset rules (restrict creations/updates/deletions, require linear history, signed commits, pull request with approvals, code owner review and stale-approval dismissal, status checks with the strict up-to-date option, block force pushes), bypass lists, and the "Evaluate" mode; the REST path `/repos/{owner}/{repo}/rulesets` in the GitHub OpenAPI description (used by `gh api`); the Terraform `github_repository_ruleset` resource; GitLab server hooks and the `custom_hooks` archive. Removed as unconfirmed: the `rev-list --not --all` suggestion, the required-checks and pre-receive timeout gotchas and the Azure DevOps remark.

Method: documentation only; no commands were run.
