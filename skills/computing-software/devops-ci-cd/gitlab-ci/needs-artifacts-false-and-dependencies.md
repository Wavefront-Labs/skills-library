---
id: computing-software.devops-ci-cd.gitlab-ci.needs-artifacts-false-and-dependencies
name: needs-artifacts-false-and-dependencies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, needs-artifacts-false, dependencies-keyword, artifact-download-control, empty-dependencies]
level: practitioner
status: docs-checked
description: "Stop jobs downloading artifacts they do not need with needs artifacts false or dependencies: [], and how needs and dependencies interact."
sources: ["https://docs.gitlab.com/ci/yaml/#needsartifacts", "https://docs.gitlab.com/ci/yaml/#dependencies", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# needs: artifacts: false and dependencies

By default a job with `needs` downloads artifacts from the jobs listed in `needs`, and a job without `needs`
or `dependencies` downloads artifacts from **all jobs in earlier stages**. Unneeded downloads waste time.

## 1. Ordering without artifacts
```yaml
e2e:
  needs:
    - job: build-image          # wait for it...
      artifacts: false          # ...but don't download its artifacts
    - job: build-fixtures       # do download these
  script: echo "run end-to-end tests"
```

## 2. Stage-based pipelines: dependencies
```yaml
notify:
  stage: post
  dependencies: []             # download nothing
  script: echo "notify"
package:
  stage: package
  dependencies: [compile]      # only compile's artifacts
```

## 3. Interaction rules
- The docs say not to combine `needs` and `dependencies` in the same job.
- `dependencies` jobs must be in earlier stages; to fetch artifacts from a job in the same stage use `needs:artifacts`.
- `dependencies: []` downloads no artifacts.
- If a dependency's artifacts expired or were deleted, the job fails. Artifacts expire after 30 days by default; set `artifacts:expire_in` to cover later manual jobs.
- If the earlier job produced no artifacts, or is a manual job that did not run, the dependent job still runs without error.
- With `needs` on a `parallel` job, artifacts of all generated jobs are downloaded and same-named files overwrite each other (last download wins).

## Verify
- [ ] Lint and notify jobs download no artifacts.
- [ ] Deploy jobs still get exactly the files they ship.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md (`needs:artifacts`, `dependencies`, `artifacts:expire_in`) and doc/ci/caching/_index.md (30-day default expiry): `needs` downloads only listed jobs' artifacts, `artifacts: true|false`, `dependencies` semantics including `[]`, same-stage restriction, advice not to combine `needs` and `dependencies`, expired-artifact failure, and parallel-job overwrite. Removed the 2 GB figure, the error strings, the retry and last-successful-run claim and the log-line advice, which no page states.

Method: documentation only; no commands were run.
