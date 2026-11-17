---
id: computing-software.devops-ci-cd.gitlab-ci.merge-request-pipelines-and-rules
name: merge-request-pipelines-and-rules
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, merge-request-pipelines, merged-results-pipelines, merge-trains, rules, workflow-rules, rules-if, rules-changes, compare-to, rules-exists, when-never, when-manual, allow-failure, ci-pipeline-source, ci-merge-request-iid, ci-merge-request-target-branch-name, detached-pipeline, fork-pipelines, pipeline-must-succeed, monorepo, path-filtering, auto-cancel, interruptible]
level: advanced
status: docs-checked
description: "Get GitLab MR pipelines right: rules evaluation order, changes/compare_to for monorepos, merged-results pipelines and merge trains, fork MRs, and the blocked-manual-job trap."
sources: ["https://docs.gitlab.com/ee/ci/pipelines/merge_request_pipelines.html", "https://docs.gitlab.com/ee/ci/pipelines/merged_results_pipelines.html", "https://docs.gitlab.com/ee/ci/pipelines/merge_trains.html", "https://docs.gitlab.com/ee/ci/jobs/job_rules.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Merge request pipelines and rules

**Goal:** every MR gets exactly the jobs it needs, tested against what `main` will look
like after merge, and `main` never goes red because two MRs were green separately.

(Baseline `workflow:rules` to avoid duplicate branch+MR pipelines is in
`computing-software.devops-ci-cd.gitlab-ci.pipelines-runners-and-environments`; this
skill goes past it.)

## 1. How `rules:` evaluate
- Rules are checked **top to bottom; the first match wins** and decides `when`,
  `allow_failure`, `variables`, `needs`. No match → job is **not added**.
- A rule with no `if/changes/exists` always matches — use it as the explicit default last line.
```yaml
.mr-or-main:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
    - when: never
```
Useful variables only present in MR pipelines: `CI_MERGE_REQUEST_IID`,
`CI_MERGE_REQUEST_TARGET_BRANCH_NAME`, `CI_MERGE_REQUEST_SOURCE_BRANCH_NAME`,
`CI_MERGE_REQUEST_LABELS`, `CI_MERGE_REQUEST_EVENT_TYPE` (`detached`, `merged_result`, `merge_train`).

## 2. Path filtering for monorepos
```yaml
api-test:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes:
        paths: [services/api/**/*, libs/shared/**/*]
        compare_to: refs/heads/main
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH   # always run on main
```
- In MR pipelines, `changes:` is reliable. In branch pipelines it compares with the previous push;
  for a new branch, or when there is no Git push event (tag, scheduled, manual pipelines), it
  evaluates **true** and the job always runs. `compare_to:` fixes that when you need those pipelines.
- Caveat: in merged results pipelines the base for `compare_to` is the temporary merged commit, so
  it can match files that changed on the target branch; drop `compare_to` there or use narrower paths.
- Always run the full suite on `main` (or nightly); path filters will eventually miss
  a cross-package dependency.
- `exists:` checks file presence (e.g. run `docker-build` only if a `Dockerfile` exists) — good in shared templates.

## 3. Merged results pipelines
Enable *Settings › Merge requests › Merge options › Enable merged results pipelines* (Premium, Ultimate; Maintainer role). The MR pipeline
then runs on a temporary merge commit of source + current target. Catches "green on my
branch, red after merge". Needs `workflow:rules` that allow `merge_request_event`.
If the source branch conflicts with the target, GitLab runs a standard merge request pipeline instead.

## 4. Merge trains
*Settings › Merge requests › Merge trains* (Premium, Ultimate). MRs queued to merge each get a
pipeline on target + every MR ahead in the train; a failure drops that MR and restarts
the ones behind it.
- Keep train pipelines **fast** — every failure restarts work. Put slow suites on `main` post-merge.
- Jobs can detect train runs: `if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"`.
- Pair with *Pipelines must succeed*.

## 5. The blocked-manual trap
A `when: manual` job defaults to `allow_failure: true`, but with `rules:when: manual` the default
changes to `allow_failure: false` → the pipeline shows "blocked"
and "pipelines must succeed" never passes. Set it explicitly for optional manual jobs:
```yaml
perf-test:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      when: manual
      allow_failure: true
```

## 6. Fork MRs
Pipelines for fork MRs run in the **fork's** project by default, using the fork's CI/CD
configuration, resources and variables. Project members in the parent can trigger a pipeline in
the parent project (*Run pipeline* on the MR); it uses the fork branch's CI/CD configuration, and
fork code could try to steal parent secrets, so review the diff (especially `.gitlab-ci.yml`) first.

## 7. Cost and noise control
- `default: interruptible: true` + *Auto-cancel redundant pipelines* so a new push cancels the old run.
- Label-driven extras: `if: $CI_MERGE_REQUEST_LABELS =~ /run-e2e/`.
- Draft MRs: `if: $CI_MERGE_REQUEST_TITLE =~ /^(\[Draft\]|\(Draft\)|Draft:)/` → `when: manual`.

## Uncertainty
Not hands-on verified; check the docs for your GitLab version.

## Verify
- [ ] Each job's rules end in an explicit default; no job vanishes unexpectedly (check the MR pipeline graph).
- [ ] Path-filtered jobs still run on `main`; `compare_to` used where branch pipelines exist.
- [ ] MR pipeline label shows "merged results" (or train) once enabled.
- [ ] No MR pipeline sits "blocked" on an optional manual job.
- [ ] Fork MR pipelines don't receive protected variables unless a maintainer explicitly triggers them.

## Checked
2026-10-31. Confirmed in the GitLab docs pages for merge request pipelines, merged results pipelines, merge trains, job rules, the CI/CD YAML reference and predefined variables: first-match rule evaluation, `CI_MERGE_REQUEST_EVENT_TYPE` values (`detached`, `merged_result`, `merge_train`), `rules:changes` true for new branches, `compare_to` caveat, Premium/Ultimate tiers, conflict fallback, the manual-job `allow_failure` default, fork behaviour.
Removed: the `rules`/`only` mixing line and the interruptible-trains advice (not found in the docs).
Method: documentation only; no commands were run.
