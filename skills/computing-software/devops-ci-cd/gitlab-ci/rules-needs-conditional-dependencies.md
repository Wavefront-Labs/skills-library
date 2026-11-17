---
id: computing-software.devops-ci-cd.gitlab-ci.rules-needs-conditional-dependencies
name: rules-needs-conditional-dependencies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, rules-needs, conditional-needs, dynamic-needs]
level: advanced
status: docs-checked
description: "Change a job's needs per condition with rules:needs, e.g. waiting for a full build on main but only a quick build on MRs, and how it replaces job-level needs."
sources: ["https://docs.gitlab.com/ci/yaml/#rulesneeds"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# rules:needs

## 1. Pattern
```yaml
build-quick:
  rules: [{ if: $CI_PIPELINE_SOURCE == "merge_request_event" }]
  script: make build-debug

build-full:
  rules: [{ if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH }]
  script: make build-release

test:
  needs: [build-quick]                       # default
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      needs: [build-full]                    # replaces job-level needs on main
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
  script: make test
```
`rules:needs` **replaces** the job's `needs` when that rule matches; non-matching rules keep the job-level list.

## 2. Forms
- `rules:needs` takes the same kind of job list as job-level `needs` (see the CI YAML reference for the full forms).

## 3. Versus alternatives
- `needs:optional` handles "depend if present"; `rules:needs` handles "depend on something else
  under condition X". Often `optional` is enough and simpler.

## 4. Gotchas
- Needed jobs must exist in the pipeline for that condition, or pipeline creation can fail (use `needs:optional` where a job may be absent); test every branch type with the pipeline editor's **Validate** tab.

## Verify
- [ ] Validate tab simulation for `main` and for an MR shows different dependency edges.

## Checked

2026-10-28. Confirmed on the CI YAML rules:needs section: needs in rules updates a job's needs when a condition matches, and needs:optional resolves pipeline creation failures for jobs excluded by rules. Removed: the 16.4 version claim, the full-form and empty-list claims, the stage-ordering fallback, and the exact error message.
Method: documentation only; no commands were run.
