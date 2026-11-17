---
id: computing-software.devops-ci-cd.gitea.protected-branches
name: protected-branches
category: computing-software
field: devops-ci-cd
product: gitea
tags: [gitea-branch-protection, gitea, protected-branch-pattern, status-check-patterns, required-approvals, force-push-allowlist, protected-file-patterns, block-on-outdated-branch]
level: advanced
status: docs-checked
description: "Configure Gitea protected branch rules: glob patterns and priority, push and force-push allowlists, deletion, merge approvals, status checks, signed commits, file patterns."
sources: ["https://gitea.com/gitea/docs/src/branch/main/docs/usage/access-control/protected-branches.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Gitea protected branches

Rules apply to HTTP(S) and SSH Git, the web editor, the API and background jobs such as auto-merge. Managed by repository owners and admins under **Settings, Branches**, **Add new rule**; the page is read-only for archived repos. A rule applies immediately to matching branches, including ones created later.

## Matching and priority
The pattern is a gobwas glob against the whole branch name, case-sensitive (a plain name like `main` with no glob characters matches that branch case-insensitively). If several rules match, **only the first** applies; drag to reorder, priority 1 on top, so put `main` or `release/*` before a fallback `*`. Examples: `release/*` (`release/v1.0`), `hotfix/**` (nested), `*` (every branch).
**Protected file patterns** (semicolon separated, case-insensitive, e.g. `.drone.yml` or `/docs/**/*.txt`) reject pushes and block merges that touch those paths. **Unprotected file patterns** let write users push changes that touch only those files even when pushes are disabled.

## Pushes, force pushes, deletion
- Push: **Disable push** (PRs only), **Enable push** (anyone with write access; force push still blocked), or **Allowlist restricted push** (users, and teams for org repos). Allowlists may include the **Gitea Actions** and **Deploy Key** system users (they still need write access; Deploy Key also covers deploy tokens).
- Force push: disable, enable (for anyone who can push), or allowlist (separate list **and** regular push access).
- Branch deletion: disabled by default; enable, or allowlist (plus push access). Applies to `git push --delete`, API, UI and post-merge cleanup. The default branch and the default PR target can never be deleted.

## Merge gates
Merge allowlist (default: any writer), **required approvals** (count; only write-access reviews count unless approvals are restricted to an allowlist), **dismiss stale approvals** (new commits that change the PR drop approvals), **ignore stale approvals** (keep but do not count old-commit reviews; disabled while dismiss is on), **block merge on rejected reviews**, **block merge on official review requests** (e.g. CODEOWNERS), **block merge if the PR is outdated** (head must contain the base), and **Administrators must follow branch protection rules** (removes admins' Force merge bypass).

## Status checks
Tick **Enable status check** and list glob patterns, one per line (e.g. `actions/test-*`), matching context names reported by Actions, Drone, Woodpecker or any Check API client. At least one context per pattern must succeed on the head commit. An empty list is not allowed; use `*` to require success of the latest commit whatever the name. The helper table shows contexts reported in the last week.

## Signed commits
**Require signed commits** rejects unsigned or unverifiable commits in the server-side hook (see `gitea-signing-key` for server signing).

## Checked
2026-11-03. Commands, flags, settings, numbers and behaviour were compared line by line with the Gitea docs source page named in `sources` (read in full from the docs repository raw file). Nothing else removed; no unconfirmed claim remained.
Method: documentation only; no commands were run.
