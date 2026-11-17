---
id: computing-software.devops-ci-cd.gitlab-ci.auto-merge-when-pipeline-succeeds
name: auto-merge-when-pipeline-succeeds
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, merge-when-pipeline-succeeds, auto-merge, glab-mr-merge, merge-checks]
level: intro
status: docs-checked
description: "Use auto-merge (formerly merge when pipeline succeeds) from the UI, glab and the API, with the merge checks it waits for and how to cancel it."
sources: ["https://docs.gitlab.com/user/project/merge_requests/auto_merge/", "https://docs.gitlab.com/api/merge_requests/#merge-a-merge-request"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Auto-merge when the pipeline succeeds

## 1. What it waits for
Auto-merge merges the MR once all merge checks pass: required approvals, no blocking MRs, no conflicts, a successful pipeline, resolved discussions, not a Draft, external status checks passed, no denied policies. The auto-merge page lists the full set.
If the pipeline fails, the author can retry failed jobs (a successful retry merges) or push fixes. Pushing new commits to the MR cancels auto-merge so the changes get reviewed.

## 2. Set it
- UI: **Set to auto-merge** button.
- Command line: use the `merge_request.merge_when_pipeline_succeeds` push option.
- API:
```bash
curl -X PUT -H "PRIVATE-TOKEN: $T" \
  "$API/projects/$PID/merge_requests/$IID/merge?auto_merge=true"
curl -X POST -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/merge_requests/$IID/cancel_auto_merge"
```
With merge trains enabled, auto-merge adds the MR to the train when checks pass.

## 3. Gotchas
- "Pipelines must succeed" requires a successful pipeline; a merge request with no pipeline cannot merge, so make sure pipelines run for every MR.
- If new commits reach the target branch and the project uses semi-linear history or fast-forward merge without automatic rebase, GitLab cancels the request; with automatic rebase it stays active.
- Needs the Developer, Maintainer or Owner role.

## Verify
- [ ] The MR shows it is set to merge automatically and merges after the checks pass.

## Checked

2026-10-28. Confirmed on the auto-merge page and the merge requests API page: the list of merge checks, retry behaviour after a failed pipeline, new commits cancelling auto-merge, the merge_request.merge_when_pipeline_succeeds push option, auto_merge=true on the merge endpoint, cancel_auto_merge (the page says to use it instead of cancel_merge_when_pipeline_succeeds), Pipelines must succeed behaviour, semi-linear/fast-forward cancellation, Developer role. Corrected the draft's claims that a failed pipeline cancels auto-merge and that a new push keeps it set. Removed: glab command and flags, should_remove_source_branch, Renovate section, approval-reset and merge-train details not on the page.
Method: documentation only; no commands were run.
