---
id: computing-software.devops-ci-cd.concourse-ci.across-limitations-and-dynamic-pipelines
name: across-limitations-and-dynamic-pipelines
category: computing-software
field: devops-ci-cd
product: concourse-ci
tags: [across, limitations, get-step, set-pipeline, instance-vars, multi-branch, validation]
level: advanced
status: docs-checked
description: "Know what across cannot do (no get or put with interpolated names, as inputs are fixed before a job starts) and how to set one pipeline per branch with across plus set_pipeline."
sources:
  - https://concourse-ci.org/docs/steps/modifier-and-hooks/across/
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
**Limitation.** `across` does not work with `get` or `put`. Resource names are not interpolated inside across steps, so this fails:

```yaml
- across:
    - var: version
      values: [ "1.16", "1.17" ]
  do:
    - get: go-((.:version))
```

The reason is that Concourse determines a job's inputs before the job starts, and cannot discover inputs while a build is running. Pipeline validation also blocks it, since it checks the relationship between all resources and jobs by looking at `get` and `put` steps. Setting such a pipeline gives an error like `jobs.job.plan.do[0].across.get(go): unknown resource 'go-((.:version))'`. Declare the resources explicitly instead.

**What it does combine with.** `across` plus `set_pipeline` plus `instance_vars` keeps one pipeline per item. The documented multi-branch plan fetches a resource that lists branches, loads them, and iterates:

```yaml
plan:
  - get: release-branches
    trigger: true
  - get: ci
  - load_var: branches
    file: release-branches/branches.json
  - across:
      - var: branch
        values: ((.:branches))
    set_pipeline: release
    file: ci/pipelines/release.yml
    instance_vars: { branch: ((.:branch.name)) }
```

A new branch creates a new pipeline. A deleted branch's pipeline is archived automatically, following the `set_pipeline` auto-archive rule.

## Checked

2026-11-04. Limitation, error text and multi-branch example confirmed on the Across Step Modifier page (Limitations, Examples).

Method: documentation only; no commands were run.
