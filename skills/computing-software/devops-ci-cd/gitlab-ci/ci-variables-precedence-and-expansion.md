---
id: computing-software.devops-ci-cd.gitlab-ci.ci-variables-precedence-and-expansion
name: ci-variables-precedence-and-expansion
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-variables, variable-precedence, predefined-variables, variable-expansion, file-variables, protected-variables, masked-variables, masked-and-hidden, group-variables, instance-variables, environment-scoped-variables, variables-keyword, pipeline-variables, ci-commit-ref-slug, ci-pipeline-source, variables-description, variables-options]
level: practitioner
status: docs-checked
description: "Master GitLab CI/CD variables: the precedence order, key predefined CI_* values, expansion, file-type variables, protected, masked and hidden flags, environment scope."
sources: ["https://docs.gitlab.com/ci/variables/", "https://docs.gitlab.com/ci/variables/predefined_variables/", "https://docs.gitlab.com/ci/variables/where_variables_can_be_used/", "https://docs.gitlab.com/ci/yaml/#variables"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI/CD variables: precedence and expansion

**Goal:** know which value a job actually sees, keep secrets out of logs and unprotected
branches, and pass values between jobs without surprises.

## 1. Precedence (highest first)
1. Pipeline execution policy or scan execution policy variables (only for jobs a policy adds)
2. Manual job variables set when you run a manual job
3. Pipeline variables: Run pipeline page, pipeline schedule, pipelines API, triggers API,
   `ci.variable` push option, upstream pipeline
4. Project variables
5. Group variables (the closest subgroup wins)
6. Instance variables
7. dotenv report variables from jobs in `dependencies` or `needs`
8. `.gitlab-ci.yml` variables, highest first: `rules:variables`, job `variables`,
   `workflow:rules:variables`, top-level default variables
9. Deployment variables
10. Predefined variables (but `CI_ENVIRONMENT_ID`, `CI_ENVIRONMENT_SLUG`,
    `CI_ENVIRONMENT_URL` and `CI_PAGES_URL` cannot be overridden)

So a project variable beats anything in the YAML file, and a Run pipeline variable beats a
project variable. Secrets fetched from an external secrets manager are outside this order, and
`spec:inputs` inputs are not variables and take no part. Pipeline inputs are recommended over
pipeline variables (17.7+); consider disabling pipeline variables when you use inputs.
`variables:description` and `variables:options` (see the YAML reference) describe a value and
offer a dropdown on the Run pipeline page.

## 2. Predefined variables worth knowing
- `CI_PIPELINE_SOURCE`: how the pipeline was triggered.
- `CI_COMMIT_REF_SLUG`: `CI_COMMIT_REF_NAME` lowercased, shortened to 63 bytes, anything outside
  `0-9a-z` replaced with `-`, no leading or trailing `-`; for URLs and host names.
- `CI_COMMIT_SHORT_SHA`: first eight characters of `CI_COMMIT_SHA`.
- `CI_COMMIT_TAG`: only in tag pipelines. `CI_DEFAULT_BRANCH`: the project default branch.
- `CI_MERGE_REQUEST_IID` and `CI_MERGE_REQUEST_TARGET_BRANCH_NAME`: merge request pipelines only.
- `CI_JOB_TOKEN`: valid while the job runs. `CI_REGISTRY_IMAGE`: base registry address, only if the
  registry is enabled.
- `CI_OPEN_MERGE_REQUESTS`: up to four MRs for the branch. `CI_NODE_INDEX` and `CI_NODE_TOTAL`:
  parallel jobs (`CI_NODE_TOTAL` is 1 without `parallel`).

## 3. Expansion
- In `variables:` of the YAML file, `variables:expand` controls whether `$` references expand.
- Variables defined in the UI are not expanded by default (the expand option was turned
  off by default in 18.6); the checkbox is *Expand variable reference*.
- Do not mask a value you want to expand: with masking plus expansion, the only non-alphanumeric
  characters allowed are `_ : @ - + . ~ = /`.
- Where variables work is listed on the "Where variables can be used" page: `include` supports
  them (see "Use variables with include"), `rules:changes` and `rules:changes:compare_to` do not,
  `trigger` and `trigger:project` do. Variables created in a job's `script` cannot be used in
  keys like `environment:url`.

## 4. Types and flags
- **File** type (project, group and instance variables only): value saved to a temporary file and
  the variable holds its path; for tools that need a file path, such as kubectl's
  `--certificate-authority`. A variable defined in `.gitlab-ci.yml` cannot be a file type: write it
  to a file in `script`.
- **Protected**: available only to pipelines on protected branches or tags (merge request and
  merged results pipelines can optionally access them).
- **Masked**: replaced by `[MASKED]` in job logs. The value must be a single line without spaces, at
  least 8 characters, and not match the name of another variable. A value that a process outputs in
  modified form (for example with backslash escapes) is not masked. Masking does not stop a
  malicious script from reading the value; prefer external secrets. `CI_DEBUG_SERVICES` can reveal it.
- **Masked and hidden**: also hides the value in the settings UI after creation; only possible when
  creating a new variable.
- Value limit: 10,000 characters. **Environment scope**: all (`*`), a specific environment or a
  wildcard.

## 5. Passing values between jobs
Write `KEY=value` lines to a file and publish it with `artifacts:reports:dotenv`; later jobs
in `dependencies` or `needs` receive them as variables (precedence 7 above). Pass variables to a
downstream pipeline with `variables`, `trigger:forward` or dotenv.

## Verify
- [ ] Deploy secrets are protected and masked.
- [ ] `echo $CI_PIPELINE_SOURCE` matches expectations for MR, push and schedule runs.
- [ ] The value a job sees matches the precedence list above (test by running manually with an override).

## Checked
2026-10-31. Confirmed on the CI/CD variables page (precedence list, masking rules, hidden
variables, protect, file type, expansion, 10,000 characters), the Predefined variables page
(slug, short SHA, tag, open MRs, node vars) and Where variables can be used.
Corrected: the old precedence order was wrong (project variables do not outrank pipeline variables;
YAML variables rank below project, group and instance). Removed as unconfirmed: dotenv per-tier
limits, `$$` escape, job-token allowlist detail, `CI_DEBUG_TRACE`, `rules:if` null semantics,
`include:` variable restrictions, environment scope examples.
Method: documentation only; no commands were run.
