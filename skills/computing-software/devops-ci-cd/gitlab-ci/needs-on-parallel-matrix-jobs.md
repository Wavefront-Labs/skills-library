---
id: computing-software.devops-ci-cd.gitlab-ci.needs-on-parallel-matrix-jobs
name: needs-on-parallel-matrix-jobs
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, needs-parallel-matrix, matrix-job-names, parallel-matrix-dependencies]
level: advanced
status: docs-checked
description: "Make jobs depend on specific legs of a parallel:matrix job using needs:parallel:matrix, and understand the generated job names and the all-legs default."
sources: ["https://docs.gitlab.com/ci/yaml/#needsparallelmatrix", "https://docs.gitlab.com/ci/yaml/matrix_expressions/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/yaml/matrix_expressions.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# needs on parallel:matrix jobs

## 1. Generated names
```yaml
build:
  parallel:
    matrix:
      - PROVIDER: [aws, gcp]
        ARCH: [amd64, arm64]
  script: echo "build $PROVIDER $ARCH"
```
Creates `build: [aws, amd64]`, `build: [aws, arm64]`, `build: [gcp, amd64]`, `build: [gcp, arm64]`. Values are appended to the job name in the order the matrix variables are declared. The matrix can create at most 200 permutations; identifiers use only letters, numbers and underscores.

## 2. Depend on all legs vs one leg
```yaml
publish-all:
  needs: [build]                      # depends on ALL generated build jobs, and downloads artifacts from all of them
deploy-aws:
  needs:
    - job: build
      parallel:
        matrix:
          - PROVIDER: aws
            ARCH: [amd64, arm64]      # only the two aws legs
  script: echo "deploy aws"
```
With `needs:parallel:matrix` the identifiers and values must come from the matrix defined in the needed job, and the order of identifiers must match the order in that job (reversed order is invalid). Artifacts with the same name from several legs overwrite each other, so only the last download is kept.

## 3. Matrix to matrix (leg N needs leg N)
Matrix expressions (GitLab 18.6) create a 1:1 mapping without listing every combination:
```yaml
test:
  parallel:
    matrix:
      - PROVIDER: [aws, gcp]
        ARCH: [amd64, arm64]
  needs:
    - job: build
      parallel:
        matrix:
          - PROVIDER: ['$[[ matrix.PROVIDER ]]']
            ARCH: ['$[[ matrix.ARCH ]]']
  script: echo "test $PROVIDER $ARCH"
```
Matrix expressions are resolved when the pipeline is created, are plain string replacement, and can reference only matrix identifiers (not CI/CD variables or inputs).

## 4. Gotchas
- You cannot combine `needs:parallel:matrix` with `needs:optional`.
- Each job in a matrix counts toward the `needs` limit (50 jobs per job on GitLab.com; the default for Self-Managed and Dedicated, adjustable by an administrator in the CI/CD limits).
- Matrix entries with identical values but different identifier names generate identical job names and overwrite each other.

## Verify
- [ ] The pipeline graph in the Job dependencies view connects `deploy-aws` only to the aws jobs.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/yaml/_index.md, doc/ci/yaml/matrix_expressions.md and doc/ci/jobs/job_control.md: generated job names such as `linux:build: [aws, app1]`, `needs` on a parallelized job depends on all its jobs and downloads artifacts from all of them (same-named artifacts overwrite each other), `needs:parallel:matrix` for a subset with identifiers taken from the matrix job and in the same order, no combination with `needs:optional`, matrix expressions `$[[ matrix.IDENTIFIER ]]` (GitLab 18.6) for 1:1 mapping, the limit of 50 jobs in `needs`, and the 200-permutation cap. Removed the `$PROVIDER` expansion claim (16.3), the pipeline-creation-error and name-quoting claims, the `dependencies:` remark and the Job dependencies view claim for this case.

Method: documentation only; no commands were run.
