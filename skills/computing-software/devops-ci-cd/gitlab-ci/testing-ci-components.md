---
id: computing-software.devops-ci-cd.gitlab-ci.testing-ci-components
name: testing-ci-components
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, component-testing, component-self-test, component-pipeline-assertions]
level: advanced
status: docs-checked
description: "Test CI/CD components in their own project pipeline: include them at the current SHA, assert job outcomes and generated jobs, and gate releases on those tests."
sources: ["https://docs.gitlab.com/ci/components/#test-the-component", "https://docs.gitlab.com/api/lint/", "https://github.com/gitlabhq/gitlabhq/blob/master/doc/ci/components/_index.md"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Testing CI components

## 1. Include yourself at the commit under test
```yaml
# component project .gitlab-ci.yml
include:
  - component: $CI_SERVER_FQDN/$CI_PROJECT_PATH/pytest@$CI_COMMIT_SHA
    inputs:
      stage: test
      job-prefix: "selftest-"
      coverage-min: 0

stages: [test, verify, release]
```
Components that need source files can be tested against sample files kept in the component project (see the testing section of the components docs).

## 2. Assert the result
```yaml
verify-jobs-exist:
  stage: verify
  image: badouralix/curl-jq
  script:
    - |
      route="${CI_API_V4_URL}/projects/${CI_PROJECT_ID}/pipelines/${CI_PIPELINE_ID}/jobs"
      count=`curl --silent --header "JOB-TOKEN: ${CI_JOB_TOKEN}" "$route" | jq 'map(select(.name | contains("selftest-pytest"))) | length'`
      if [ "$count" != "1" ]; then exit 1; else echo "Component job present"; fi
```
This follows the example in the components docs: it reads the pipeline's jobs through the API with `CI_JOB_TOKEN`
and fails unless the component's job is present. Use `$CI_API_V4_URL` rather than a hardcoded host. You can also inspect data the component generates.
Authentication is necessary if the project is private.

## 3. Lint all input combinations
`POST /projects/:id/ci/lint` validates configuration in the context of a project. It takes `content` (required), `dry_run`
(pipeline creation simulation instead of a static check, default `false`), `include_jobs` and `ref`, with a JSON body:
```bash
curl --request POST --header "PRIVATE-TOKEN: <your_access_token>" --header "Content-Type: application/json" \
  --data '{"content": "<escaped YAML>", "dry_run": true}' "https://gitlab.example.com/api/v4/projects/<id>/ci/lint"
```
The response contains `valid` and `errors`. Run it for each example configuration in the README.

## 4. Gate releases
The docs recommend configuring the tag pipeline to test the components before the release job runs (stage order or `needs`), so a broken component is not released.

## Verify
- [ ] MR pipeline of the component project runs the self-test jobs with the MR's code.
- [ ] A deliberately broken template makes the self-test pipeline fail before the release job.

## Checked

2026-10-25: GitLab documentation as published in the gitlabhq/gitlabhq doc/ tree (development head, last commit 2026-10-23). Confirmed in doc/ci/components/_index.md and doc/api/lint.md: the self-include at `$CI_COMMIT_SHA`, the job-count check via `CI_JOB_TOKEN` and the pipeline jobs API (taken from the docs example), tests before the release job, sample files in the component project, and the CI Lint endpoint (`content`, `dry_run`, `include_jobs`, `ref`, JSON body, `valid` in the response). Removed the alpine/apk tooling, the negative-test child-pipeline advice and the fixture directory name, which no page states.

Method: documentation only; no commands were run.
