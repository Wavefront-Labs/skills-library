---
id: computing-software.cloud-infrastructure-engineering.azure.azure-repos-branch-policies-and-branching-strategy
name: azure-repos-branch-policies-and-branching-strategy
category: computing-software
field: cloud-infrastructure-engineering
product: azure
tags: [azure, azure-devops, azure-repos, branch-policies, pull-requests, branch-strategy, trunk-based, release-flow, gitflow, required-reviewers, build-validation, status-checks, comment-resolution, work-item-linking, merge-strategies, squash-merge, semi-linear, auto-complete, branch-permissions, cross-repo-policies, repo-security, git-lfs, monorepo, code-owners, pr-templates]
level: practitioner
status: docs-checked
description: "Set up Azure Repos for safe flow: trunk-based or release-flow branching, branch policies (reviewers, build validation, status checks), merge strategies, permissions."
sources: ["https://learn.microsoft.com/azure/devops/repos/git/branch-policies", "https://learn.microsoft.com/cli/azure/repos/policy/build", "https://learn.microsoft.com/cli/azure/repos/policy/required-reviewer"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Azure Repos — branching strategy and the policies that make `main` always releasable

**Goal:** short-lived branches merged through PRs that are built, reviewed, linked to
work and squashed into a linear `main`; releases cut from tags or release branches
with the same policies; no direct pushes anywhere that matters.

## 1. Strategy
- **Trunk-based** (default for services with CD): `main` protected; feature branches `feature/<id>-<slug>` live < 3 days; releases = tags on `main` (`v2026.10.14`) deployed by pipeline; hotfix = fix forward on `main`.
- **Release flow** (Microsoft's own model for products with supported versions): `main` + `release/<version>` branches cut per release; fixes go to `main` first then cherry-pick to `release/*` (PR with `cherry-pick` button). Use when you ship multiple supported versions or need a stabilisation window.
- Avoid Gitflow (`develop` + long-lived release branches) unless you genuinely need it — it doubles merge work and hides integration problems.
- Branch naming via policy-less convention + permission on `refs/heads/feature/*` for everyone, `refs/heads/release/*` for release managers; folder-style names show as a tree in the UI.

## 2. Branch policies on `main` (and `release/*`)
```bash
az repos policy approver-count create --repository-id <repo> --branch main --minimum-approver-count 1 --creator-vote-counts false --allow-downvotes false --reset-on-source-push true --blocking true --enabled true
az repos policy build create --repository-id <repo> --branch main --build-definition-id <pipeline-id> --display-name "PR build" --valid-duration 720 --queue-on-source-update-only true --manual-queue-only false --blocking true --enabled true
az repos policy work-item-linking create --repository-id <repo> --branch main --blocking true --enabled true
az repos policy comment-required create --repository-id <repo> --branch main --blocking true --enabled true
az repos policy merge-strategy create --repository-id <repo> --branch main --allow-squash true --allow-no-fast-forward false --allow-rebase false --allow-rebase-merge false --blocking true --enabled true
az repos policy required-reviewer create --repository-id <repo> --branch main --required-reviewer-ids "<reviewer-email>;<reviewer-email>" --message "Platform review" --path-filter "/infra/*;/.azure-pipelines/*" --blocking true --enabled true
```
- **Minimum reviewers** (1 for most repos, 2 for platform/infra), *reset votes on new push*, *prohibit the most recent pusher from approving*.
- **Build validation**: the PR pipeline (`pr:` triggers aren't used for Azure Repos — this policy is the PR trigger), expiry 12 h, auto-queue on push.
- **Status checks**: external gates post a status via the REST API — security scan, licence check, preview-environment smoke; make them required.
- **Comment resolution** required; **work item linking** required (traceability to Boards); **automatically included reviewers** with path filters for sensitive paths (the CODEOWNERS equivalent); **limit merge types** to squash (linear history, one commit per PR) or semi-linear if you want to keep PR commits.
- **Cross-repo policies** (Project settings → Repositories → Policies → *Default branch* / branch pattern `release/*`): apply the baseline to every repo, including new ones.
- Bypass: grant *Bypass policies when completing pull requests* only to a break-glass group with PIM; audit bypass events in the audit log.

## 3. PR hygiene
- PR template with checklist: tests, migrations, rollback, docs.
- **Auto-complete** with squash + delete source branch + complete linked work items; draft PRs for early feedback; `@mention` + suggested changes; *required* vs *optional* reviewers.
- Keep PRs < 400 lines; stacked PRs for bigger changes. Rely on *reset votes on push* plus build validation rather than a merge queue.
- Branch cleanup: delete the source branch on completion; list branches with `az repos ref list --filter heads/`.

## 4. Repository security and settings
- Project settings → Repositories → Settings and Policies: review the repository-level policies the portal offers (file size, path, secrets push protection) and use **Git LFS** for binaries: `git lfs track "*.psd"`.
- Permissions: *Contribute* to developers on feature refs, `main`/`release/*` **Contribute: Deny** for everyone except the build service (merges happen via PR completion by the service); *Force push: Deny*; *Create branch* allowed; *Manage permissions* to admins; project-level *Edit policies* restricted.
- Build service identity: *Limit job authorization scope* (pipelines skill) + repo-level *Contribute* for the pipeline that tags releases.
- Default branch `main` (org-level default for new repos); `.gitattributes` for line endings.

## 5. Monorepo vs many repos
- Many repos: simpler policies per service, template repo for pipelines; use **cross-repo policies** and a repo-creation script (`az repos create` + policy set) so every repo starts governed.
- Monorepo: path filters on build validation (`--path-filter`) and required reviewers; pipelines with `trigger.paths`; code search scoped by path; be aware of PR build fan-out and branch-policy evaluation per path.

## Gotchas
- Build validation policies target a pipeline *definition*; renaming/moving the pipeline breaks the policy silently (shows as "policy not applicable").
- Squash merge rewrites history — a branch that was based on another unmerged branch gets conflicts; teach *rebase onto main* before PR.
- Required reviewers with path filters match on the PR's **changed files**; moving a file out of the path bypasses it — pair with cross-repo policy and audit.
- Work-item linking policy accepts any work item; it doesn't check type/state — add a status check for "linked item in Active/Approved" if that matters.
- Bypass policy on completion leaves a bypass reason — alert on it (`az devops` audit stream to Log Analytics/Sentinel).
- Deleting the default branch or changing it via UI doesn't move policies — policies are per branch name (`main`), use the same name everywhere.

## Verify
- [ ] `az repos policy list --repository-id <repo> --branch main -o table` shows approver count, build validation, work item, comment resolution and merge strategy policies, all `isBlocking: true`.
- [ ] Direct `git push origin main` is rejected by policy; a PR with a failing build can't complete; a PR with an unresolved comment can't complete.
- [ ] `git log --oneline main` shows one squash commit per PR with the PR number in the subject; source branches auto-deleted.
- [ ] A new repository created this month already has the cross-repo baseline policies and `main` Contribute denied for developers.

## Checked

2026-10-28. Confirmed against Microsoft Learn pages: az repos policy build create flags (corrected to --queue-on-source-update-only), required-reviewer create flags (--message required, reviewers by email), valid-duration in minutes, reset votes and most-recent-pusher options, squash merge limit.

Removed because not confirmed: the repository settings list, audit event name, error code, refs/pull merge-commit claim, stats REST endpoint and template path.

Method: documentation only; no commands were run.
