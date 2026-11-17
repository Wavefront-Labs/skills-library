---
id: computing-software.devops-ci-cd.gitlab-ci.parent-child-and-multi-project-pipelines
name: parent-child-and-multi-project-pipelines
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, parent-child-pipelines, child-pipelines, dynamic-child-pipelines, multi-project-pipelines, downstream-pipelines, trigger-keyword, trigger-include, trigger-project, strategy-mirror, trigger-forward, pipeline-variables-forward, generated-yaml, monorepo-pipelines, needs-pipeline, cross-project-artifacts, ci-job-token-allowlist, ci-pipeline-source-pipeline, parent-pipeline, inputs-to-child]
level: advanced
status: docs-checked
description: "Split GitLab pipelines: parent-child with static or generated YAML, multi-project triggers, strategy mirror, variable and input passing, cross-project artifacts."
sources: ["https://docs.gitlab.com/ci/pipelines/downstream_pipelines/", "https://docs.gitlab.com/ci/yaml/#trigger", "https://docs.gitlab.com/ci/jobs/ci_job_token/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Parent-child and multi-project pipelines

**Goal:** a monorepo whose pipeline only builds what changed, and service repos that kick
off an integration or deploy pipeline elsewhere, with status flowing back to the MR.

## 1. Parent-child (same project)
```yaml
frontend:
  trigger:
    include: frontend/.gitlab-ci.yml
    strategy: mirror          # trigger job always has the downstream pipeline's status
  rules:
    - changes: [frontend/**/*]
backend:
  trigger:
    include:
      - local: backend/.gitlab-ci.yml
      - project: group/ci-templates
        ref: main
        file: /go.yml
    strategy: mirror
  rules:
    - changes: [backend/**/*]
```
- Child pipelines run under the same project, ref and commit SHA as the parent. They do not
  affect the ref's status unless triggered with `trigger:strategy`, and appear only on the
  parent's details page, not in the project pipeline list.
- A trigger job does not use a runner. It shows passed once the downstream pipeline is created
  (failed if creation fails), unless you set `strategy`. GitLab does not recommend
  `strategy: depend`, because the trigger job status does not always match the downstream status;
  use `mirror`.
- Up to three configuration files can be combined in `trigger:include`.
- Maximum depth is two levels of child pipelines. A pipeline hierarchy can hold up to 1000
  downstream pipelines by default.
- `$CI_PIPELINE_SOURCE` is `parent_pipeline` in children and `pipeline` in multi-project
  downstream pipelines. In a child, test `$CI_MERGE_REQUEST_ID` (not `merge_request_event`) to
  detect a merge request parent; the parent's `CI_MERGE_REQUEST_*` variables are passed down. Child
  pipelines run as branch pipelines unless `rules` or `workflow:rules` say otherwise.
- Child pipelines are auto-canceled if the pipeline is `interruptible` and a new pipeline starts.
- For MR widgets to show child pipeline reports (JUnit, code quality, security; 18.6+), the
  trigger job needs `strategy: depend` or `mirror`; without it the parent finishes first.

## 2. Dynamic child pipelines
```yaml
generate-config:
  stage: build
  script: generate-ci-config > generated-config.yml
  artifacts:
    paths: [generated-config.yml]
child-pipeline:
  stage: test
  trigger:
    include:
      - artifact: generated-config.yml
        job: generate-config
```
The artifact must be within instance limits, the path is parsed by GitLab (use `/`), and
CI/CD variables cannot be used in an `include` section of a dynamic child's configuration.

## 3. Multi-project (downstream in another project)
```yaml
staging:
  stage: deploy
  trigger:
    project: my/deployment
    branch: stable-11-2          # branch or tag; project and branch allow variable expansion
    strategy: mirror
```
- The user who triggers the upstream pipeline needs permission to start pipelines in the
  downstream project, otherwise the downstream pipeline fails to start.
- Multi-project pipelines affect the downstream ref's status, show in the downstream project's
  pipeline list, have no nesting limit, and are not auto-canceled by the upstream's
  `interruptible`. A public project triggering a private one still shows the downstream project
  name and pipeline status on its pipelines page.
- From a script, the job token plus the pipeline trigger API endpoint
  (`POST /projects/<id>/trigger/pipeline` with `token=$CI_JOB_TOKEN` and `ref`) makes the new
  pipeline a downstream of the calling pipeline.
- `trigger` can combine with `environment`, so the deployment shows in the upstream project.

## 4. Passing variables and inputs
- Prefer `inputs`: define `spec:inputs` in the target configuration (with `options`, `type`,
  `description`) and pass `trigger:include: - local: ... inputs: {...}` or `trigger:inputs`.
- Trigger-job `variables:` become downstream pipeline variables, as do default (top-level)
  variables; stop that with `inherit: variables: false` (or a list).
- Save predefined variables into a job variable (`UPSTREAM_BRANCH: $CI_COMMIT_REF_NAME`) to
  pass them. Do not pass masked variables downstream: masking is not carried over.
- `trigger:forward` chooses what to forward; forwarded variables are trigger variables with the
  highest precedence. dotenv variables can also be passed.

## 5. Artifacts and tokens across pipelines
- Parent to child: pass `PARENT_PIPELINE_ID: $CI_PIPELINE_ID` on the trigger job and use
  `needs: [{pipeline: $PARENT_PIPELINE_ID, job: build_artifacts}]` in the child (Premium or
  Ultimate).
- Cross-project: `needs: [{project: my/upstream_project, job: build_artifacts, ref: main,
  artifacts: true}]`. Prerequisites: the downstream project is in the upstream project's job token
  allowlist, and the triggering user has at least Reporter in the upstream project. The upstream
  job must finish first (use `needs`).
- For upstream merge request pipelines, pass `$CI_MERGE_REQUEST_REF_PATH`
  (`refs/merge-requests/<id>/head`) as the `ref`, not a branch name. This does not work for
  merged results pipelines.

## Verify
- [ ] Changing only `frontend/` runs just the frontend child.
- [ ] Child failure fails the parent trigger job (with `mirror`) and blocks the MR.
- [ ] Downstream receives the expected variables and nothing secret.
- [ ] Cross-project artifact calls succeed after allowlisting.

## Checked
2026-10-31. Confirmed on the Downstream pipelines page: ref, status, depth and 1000 limit,
mirror versus depend, CI_PIPELINE_SOURCE values, combined includes, dynamic child rules, branch
keyword, job-token trigger API, inputs, variable inheritance and forwarding, needs:pipeline and
needs:project prerequisites.
Corrected: limit was 150 and `depend` was recommended; GitLab now recommends `mirror`; parent
`workflow:rules` and variable-forward defaults removed. Removed as unconfirmed: generation
tooling ideas, lint curl, 404/403 messages, noop job advice, monorepo patterns, job-token
allowlist default-on version.
Method: documentation only; no commands were run.
