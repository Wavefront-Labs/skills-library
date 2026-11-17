---
id: computing-software.devops-ci-cd.gitlab-ci.terraform-plan-report-in-merge-requests
name: terraform-plan-report-in-merge-requests
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, terraform-report, artifacts-reports, opentofu, merge-request-widget, tfplan]
level: practitioner
status: docs-checked
description: "Publish a plan JSON as artifacts reports terraform so the merge request shows a Terraform/OpenTofu plan widget, after stripping credentials with jq."
sources: ["https://docs.gitlab.com/ci/yaml/artifacts_reports/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Terraform plan report in merge requests

**Goal:** reviewers see the planned infrastructure changes in the MR before applying.

## Job
```yaml
plan:
  stage: plan
  script:
    - tofu init
    - tofu plan -out=plan.cache
    - tofu show -json plan.cache | jq -r '(.. | select(type=="object" and has("sensitive_values")) | .sensitive_values) = {}' > tfplan.json
  artifacts:
    paths: [plan.cache]
    reports:
      terraform: tfplan.json
```
- The report is the JSON from `show -json`, named for example `tfplan.json`. GitLab's docs require you to process it with `jq` to remove credentials before upload; treat plan JSON as sensitive because it can contain variable values. The jq filter above is an illustration only; build and test one that matches your providers.
- Use the `terraform` or `tofu` binary your project uses; the key stays `reports:terraform`. The current `artifacts:reports:terraform` docs describe the file as an OpenTofu `tfplan.json`.
- Keep `plan.cache` as a normal artifact so the apply job applies exactly what was reviewed (`needs: [plan]`).

## Gotchas
- Never publish the unfiltered plan; `expire_in` the artifacts.
- The report is uploaded as an artifact, so artifact size limits apply.
- Apply only from protected branches, with a manual gate.

## Verify
Open an MR: the plan widget appears with the planned changes.

## Checked

2026-11-02. Confirmed against the GitLab `artifacts:reports` reference: `artifacts:reports:terraform` takes a `tfplan.json`, JQ processing is required to remove credentials, the report is uploaded as an artifact. Softened: widget wording and size-limit sentence, which the page does not detail. The jq filter and tofu commands are explicitly illustrative in the skill.

Method: documentation only; no commands were run.
