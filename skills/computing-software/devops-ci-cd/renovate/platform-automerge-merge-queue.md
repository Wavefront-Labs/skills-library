---
id: computing-software.devops-ci-cd.renovate.platform-automerge-merge-queue
name: platform-automerge-merge-queue
category: computing-software
field: devops-ci-cd
product: renovate
tags: [platform-automerge, merge-queue, merge-trains, renovate]
level: advanced
status: docs-checked
description: "Rely on platform-native automerge, GitHub merge queues and GitLab merge trains safely with Renovate."
sources:
  - https://docs.renovatebot.com/key-concepts/automerge/
  - https://docs.renovatebot.com/configuration-options/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`platformAutomerge` is true by default. When `automerge` is on with `automergeType` set to `pr`, Renovate asks the hosting platform to merge the PR once branch policies pass. This is faster, but you must make the platform enforce passing tests, for example GitHub's "Require status checks before merging". Otherwise the platform may merge a Renovate PR before tests finish. Set `platformAutomerge` to `false` to have Renovate do the merge itself.

If you mark `renovate/artifacts` as a required check, also set `statusCheckWhen.artifactError` to `always`, because the default only posts the check on failure and a required check that never appears blocks every PR.

GitHub merge queue with Actions: add `merge_group` to the workflow triggers.

```yaml
on:
  pull_request:
  merge_group:
```

Then enable "Allow auto-merge" in repository settings, turn on "Require merge queue" in branch protection and set the required checks. Without Actions, make your CI run on the `gh-readonly-queue/{base_branch}` branches.

GitLab merge trains: with `platformAutomerge` on (needs GitLab 17.11 or later), Renovate asks GitLab to add the MR to the train once the pipeline succeeds; with it off, Renovate adds the MR itself once all checks have passed. `rebaseWhen=auto` then resolves to `conflicted`, since the train already tests against the target head.

Branch automerge (`automergeType=branch`) only works with a merge queue or train if Renovate is on the queue's bypass list (GitHub) or allowed to push to the protected target branch (GitLab); otherwise Renovate logs a warning and creates a PR. Use `automergeType=pr` in such repositories.

## Checked

2026-11-09: read https://docs.renovatebot.com/key-concepts/automerge/ (platform-native automerge, GitHub Merge Queue and GitLab merge trains sections) and the platformAutomerge, rebaseWhen and statusCheckWhen sections of https://docs.renovatebot.com/configuration-options/. All original claims matched; added the GitLab 17.11 requirement and the branch-automerge caveat.

Method: documentation only; no commands were run.
