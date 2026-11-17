---
id: computing-software.devops-ci-cd.release-engineering.release-branch-naming-and-protection
name: release-branch-naming-and-protection
category: computing-software
field: devops-ci-cd
product: release-engineering
tags: [release-engineering, release-branch-protection, release-branches, branch-protection-rules, rulesets, backport, maintenance-branch]
level: practitioner
status: draft
description: "Name and protect release branches: release/x.y conventions, GitHub rulesets and GitLab protected branches, required checks, restricted pushes, backport flow and end-of-life."
sources:
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets
  - https://docs.gitlab.com/ee/user/project/protected_branches.html
  - https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows
licence: Apache-2.0
version: 2
updated: 2026-11-17
---
# Release branch naming and protection

## Naming
- `release/1.4` (or `release-1.4`): one branch per minor line; patch releases 1.4.1, 1.4.2 are tags on it.
- Avoid per-patch branches (`release/1.4.1`): they multiply backport targets.
- Hotfix branches (`hotfix/1.4-cve-2026-1234`) are short-lived PR branches targeting the release branch, not long-lived.
- Consistent prefix lets one rule protect all of them (`release/*`).

## Protection (GitHub rulesets)
```bash
gh api -X POST repos/ORG/REPO/rulesets --input - <<'EOF'
{ "name": "release branches", "target": "branch", "enforcement": "active",
  "conditions": { "ref_name": { "include": ["refs/heads/release/*"], "exclude": [] } },
  "rules": [
    { "type": "deletion" }, { "type": "non_fast_forward" },
    { "type": "pull_request", "parameters": { "required_approving_review_count": 2, "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": true, "require_last_push_approval": true, "required_review_thread_resolution": true } },
    { "type": "required_status_checks", "parameters": { "strict_required_status_checks_policy": true,
        "required_status_checks": [ { "context": "build" }, { "context": "test" } ] } },
    { "type": "creation" } ],
  "bypass_actors": [ { "actor_type": "Team", "actor_id": 1234, "bypass_mode": "pull_request" } ] }
EOF
```
- `creation` restricts who can create new `release/*` branches (release managers only, via bypass).
- Tag rulesets protect `v*` tags from deletion and update - released tags must be immutable.
- GitLab: Settings > Repository > Protected branches with wildcard `release/*`, allowed to merge: Maintainers; allowed to push: No one; plus protected tags `v*`.

## Backport flow
1. Fix lands on main first (unless main no longer has the code).
2. Cherry-pick to supported release branches via PR (`git cherry-pick -x <sha>` records origin). Automate with backport bots (label `backport release/1.4`).
3. Release branch CI runs the full suite; tag `v1.4.3` from the branch.

## Lifecycle
- Publish which branches are supported (support policy table) and for how long.
- At end-of-life: archive by keeping the branch read-only (ruleset blocking all pushes) rather than deleting, so tags and history stay reachable.

## Verify
- [ ] Direct push and force-push to `release/1.4` are rejected; branch creation limited to release managers.
- [ ] Released tags can't be moved or deleted.
