---
id: computing-software.devops-ci-cd.gitlab-ci.merge-train-tuning-and-skipping
name: merge-train-tuning-and-skipping
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, fast-forward-merge-trains, merge-train-skip, merge-trains-api, merge-train-settings]
level: advanced
status: docs-checked
description: "Tune merge trains: enabling them, train size and pipeline config, merging immediately vs skipping the train, enforcement levels and the merge trains API."
sources: ["https://docs.gitlab.com/ci/pipelines/merge_trains/", "https://docs.gitlab.com/api/merge_trains/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merge train settings, fast-forward and skipping

## 1. Settings (Settings → Merge requests)
- Needs the Maintainer role, a GitLab (not external) repository, merge request pipelines in your CI
  config, and **Enable merged results pipelines** plus **Enable merge trains** (Settings → Merge requests →
  Merge options).
- Optional **Merge immediately without restarting the merge train** (an experiment): lets a merge request
  skip the train via the merge API with `skip_merge_train` set to `true`. It cannot skip trains for
  fast-forward or semi-linear merge methods.
- **Maximum parallel pipelines per merge train** (GitLab 19.0 and later): default 20, minimum 1; the project
  value cannot exceed the instance limit.
- **Merge train enforcement** (GitLab 19.3 and later) levels: allow bypass (default), enforce for all
  users, enforce with Owner override.

## 2. Pipeline config
Train pipelines have `CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"`:
```yaml
workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
e2e-full:
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"     # expensive suite only on the train
```
When a pipeline ahead fails or an MR is removed, GitLab cancels the redundant pipelines behind it and starts new ones.

## 3. Merge immediately vs skip
- **Merge immediately** (without skip allowed): merges now, cancels the other train pipelines and starts a
  new train with fresh pipelines for every MR. This can use a lot of CI resources; reserve it for critical
  situations. It may be unavailable with fast-forward merges when the source branch is behind.
- With skipping allowed (`skip_merge_train`), the MR merges and the existing train pipelines are not
  canceled or restarted, but its changes were not verified against the MRs in the train.

## 4. API
```bash
curl -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/merge_trains?scope=active"
curl -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/merge_trains/merge_requests/$IID"   # position/status
curl -X POST -H "PRIVATE-TOKEN: $T" "$API/projects/$PID/merge_trains/merge_requests/$IID?auto_merge=true"
```
`scope` is `active` or `complete`. `when_pipeline_succeeds` is deprecated in GitLab 17.11 (use `auto_merge`).
By default 20 train pipelines run in parallel; later MRs wait. With enforcement on, API merges
without `auto_merge=true` get `405`.

## Gotchas
- A failed train pipeline drops the MR and restarts the pipelines behind it; it cannot be retried. Use the
  `retry` keyword for flaky jobs (a successful retry keeps the MR on the train).
- `CI_COMMIT_BRANCH` is not available in merge request pipelines.

## Verify
- [ ] The MR widget shows its merge train position (for example "2 of 3 in queue"); the `merge_trains` API lists it.

## Checked

2026-10-31. Confirmed against the GitLab merge trains page and the merge trains API page: prerequisites and settings names, skip_merge_train and its fast-forward and semi-linear limits, merge immediately behaviour, default 20 parallel pipelines and the 19.0 project setting, enforcement levels, the 405 on direct API merges, retry advice, API endpoints, the scope values active and complete, and deprecation of when_pipeline_succeeds; CI_MERGE_REQUEST_EVENT_TYPE values (merge_train) and CI_COMMIT_BRANCH availability are from the predefined variables page.
Removed: the claim that all three merge methods work with trains, the interruptible advice, the "hours of CI wasted" figure, and the temporary ref path.

Method: documentation only; no commands were run.
