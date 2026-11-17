---
id: computing-software.cloud-infrastructure-engineering.aws.codebuild-github-actions-runners-and-webhooks
name: codebuild-github-actions-runners-and-webhooks
category: computing-software
field: cloud-infrastructure-engineering
product: aws
tags: [aws, codebuild, codebuild-runner, codebuild-webhook, github-actions, self-hosted-runner, webhook-filter-groups]
level: practitioner
status: docs-checked
description: "Use CodeBuild as managed GitHub Actions self-hosted runners and configure CodeBuild webhooks with filter groups for push and pull request events, labels and overrides."
sources: ["https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner-questions.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/github-webhook.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/sample-github-action-runners-update-labels.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/action-runner-troubleshoot-webhook.html", "https://docs.aws.amazon.com/codebuild/latest/userguide/webhooks.html"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CodeBuild GitHub Actions runners and webhooks

## Managed GitHub Actions runners
1. Create a CodeBuild project with a GitHub source and a webhook filter group containing
   `EVENT` = `WORKFLOW_JOB_QUEUED` (the `workflow_job` / `queued` event).
2. In the workflow:
```yaml
jobs:
  build:
    runs-on: codebuild-app-runner-${{ github.run_id }}-${{ github.run_attempt }}
    steps:
      - uses: actions/checkout@v4
      - run: make test
```
- The first label is required: `codebuild-<project-name>-${{ github.run_id }}-${{ github.run_attempt }}`.
- Label overrides are extra labels (`runs-on` list) or the single-string form:
  `image:<environment-type>-<image-identifier>` (for example `image:arm-3.0`; custom image `image:custom-<environment-type>-<image>`),
  `instance-size:<size>` (for example `medium`), `fleet:<fleet-name>` (overrides the project's fleet), and a buildspec override.
  Single-string form: `codebuild-<project>-<run_id>-<run_attempt>-<environment-type>-<image-identifier>-<instance-size>`, or `...-fleet-<fleet-name>`.
  Labels CodeBuild does not recognise are ignored without failing the webhook.
- Give concurrent jobs different labels. GitHub routes a job to any runner with all of the job's labels, so a job with fewer labels can take the runner made for a job with more, leaving the second stuck.
- GitLab runners and Buildkite runners are also documented as CodeBuild-hosted runners.
- You can put the `WORKFLOW_JOB_QUEUED` filter group in a CloudFormation template as well.

## Webhooks for normal builds
```bash
aws codebuild create-webhook --project-name app-build --filter-groups '[
 [{"type":"EVENT","pattern":"PUSH"},{"type":"HEAD_REF","pattern":"^refs/heads/main$"}],
 [{"type":"EVENT","pattern":"PULL_REQUEST_CREATED,PULL_REQUEST_UPDATED,PULL_REQUEST_REOPENED"},
  {"type":"BASE_REF","pattern":"^refs/heads/main$"},
  {"type":"FILE_PATH","pattern":"^services/api/"}]]'
```
- A build starts if any filter group is true; a group is true when all its filters are true.
- Filter types for GitHub: `EVENT`, `ACTOR_ACCOUNT_ID`, `HEAD_REF`, `BASE_REF` (pull request events only), `FILE_PATH`, `COMMIT_MESSAGE`, `TAG_NAME` and `RELEASE_NAME` (released/prereleased events), `REPOSITORY_NAME` (global or organization webhooks only), `WORKFLOW_NAME` (workflow job queued events). `excludeMatchedPattern: true` negates a filter.
- `PULL_REQUEST_REOPENED` works with GitHub and GitHub Enterprise Server only; the RELEASED and PRERELEASED events with GitHub only.
- `FILE_PATH` and `COMMIT_MESSAGE` do not work on GitHub Enterprise Server pull request events. `FILE_PATH` is evaluated against the first 100 changed files only.
- Security: use `ACTOR_ACCOUNT_ID` filters to say which users may trigger builds, and a pull request build policy for pull requests; do not let untrusted forks run code with your project role.

## Verify
- [ ] A workflow job waits for a runner briefly, then runs in CodeBuild.
- [ ] A pull request from an actor outside the allowed list does not trigger a build.

## Checked
2026-10-28. Confirmed on the action-runner-questions, action-runner-troubleshoot-webhook, sample-github-action-runners-update-labels, github-webhook and webhooks pages: label format and overrides, routing pitfall, filter group semantics, filter types and their event restrictions, 100-file limit. Removed as unconfirmed: per-minute billing, privileged mode for Docker in jobs, build status reporting, per-account/region source credentials, `CODEBUILD_WEBHOOK_TRIGGER`, tag-push FILE_PATH remark, the old mixed `...-image:arm-3.0` label syntax.
Method: documentation only; no commands were run.
