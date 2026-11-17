---
id: computing-software.devops-ci-cd.gitlab-ci.merge-request-event-type-and-merged-results
name: merge-request-event-type-and-merged-results
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-merge-request-event-type, merged-results-pipelines, merge-request-pipelines]
level: practitioner
status: docs-checked
description: "Distinguish detached, merged_result and merge_train MR pipelines with CI_MERGE_REQUEST_EVENT_TYPE and write rules that behave correctly in each."
sources: ["https://docs.gitlab.com/ci/pipelines/merged_results_pipelines/", "https://docs.gitlab.com/ci/variables/predefined_variables/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI_MERGE_REQUEST_EVENT_TYPE and merged results pipelines

MR pipelines set `CI_PIPELINE_SOURCE == "merge_request_event"`, and
`CI_MERGE_REQUEST_EVENT_TYPE` tells you which kind:

| Value | What ran | Commit tested |
|---|---|---|
| `detached` | MR pipeline on the source branch head | source branch HEAD |
| `merged_result` | merged results pipeline | temporary merge commit of source into target |
| `merge_train` | merge train pipeline | merge train result (see GitLab's merge trains docs) |

Merged results need "Enable merged results pipelines" under Settings > Merge requests > Merge options (Maintainer or Owner; the project must be hosted on GitLab and use merge request pipelines, or MRs can get stuck or pipelines dropped).

## Rules examples
```yaml
e2e:
  rules:
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merge_train"       # full suite only on trains
    - if: $CI_MERGE_REQUEST_EVENT_TYPE == "merged_result"
      when: manual
      allow_failure: true
coverage-diff:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
      changes: { compare_to: refs/heads/main, paths: ["src/**/*"] }
```

## Gotchas
- `CI_COMMIT_SHA` in merged results is the temporary merge commit, not on any branch; use
  `CI_MERGE_REQUEST_SOURCE_BRANCH_SHA` to report status back or tag images by source commit.
- The merged commit exists in neither branch; do not deploy from it.
- `rules:changes:compare_to` with merged results compares against the temporary merged commit, so it can trigger jobs for changes that are not yours (GitLab troubleshooting); drop `compare_to` or use narrower paths.

## Verify
- [ ] An MR shows pipeline label "merged results"; a job echoing the variable prints `merged_result`.

## Checked

2026-11-02. Confirmed: `CI_MERGE_REQUEST_EVENT_TYPE` values detached / merged_result / merge_train; `CI_MERGE_REQUEST_SOURCE_BRANCH_SHA` is present only in merged results pipelines; setting location and prerequisites; temporary merged commit exists in neither branch; compare_to caveat (GitLab predefined variables and merged results docs). Removed: Premium tier claim, fork/conflict fallback, ref garbage collection, cache-slug and merge-train re-run bullets.

Method: documentation only; no commands were run.
