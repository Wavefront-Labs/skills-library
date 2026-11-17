---
id: computing-software.devops-ci-cd.gitlab-ci.preventing-skip-ci-bypass-of-policies
name: preventing-skip-ci-bypass-of-policies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, policy-skip-ci, pipeline-execution-policy, compliance-pipelines]
level: advanced
status: docs-checked
description: "Stop developers bypassing enforced GitLab security pipelines with [skip ci] by configuring skip_ci in pipeline execution and scan execution policies."
sources: ["https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/#skip_ci-type", "https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Preventing [skip ci] bypass of enforced pipelines

A commit message containing `[skip ci]` skips the regular pipeline. Policies control whether that directive is honoured for enforced jobs.

## Pipeline execution policy
```yaml
pipeline_execution_policy:
  - name: Enforce compliance jobs
    enabled: true
    pipeline_config_strategy: inject_policy
    content:
      include:
        - project: compliance/ci
          file: policy.yml
    skip_ci:
      allowed: false
      allowlist:
        users:
          - id: 123          # e.g. a release bot that commits version bumps
```
Scan execution policies have the same `skip_ci` block. When `skip_ci` is not specified, the directive is ignored for both policy types, so nobody can skip the enforced jobs. Scan execution policies with a `schedule` rule type always ignore `skip_ci`.

## Behaviour
- With skip blocked, jobs defined by the policy are always triggered, even when the commit message contains `[skip ci]`.
- Allowlisted users keep the ability to skip: use for bots that push changelog commits, otherwise
  you get pipeline loops.

## Gotchas
- Policies need the Ultimate tier.
- Bots pushing with `[skip ci]` and not allowlisted now trigger pipelines: check for loops
  (a release job that commits and re-triggers itself).

## Verify
- [ ] Push a commit with `[skip ci]` as a normal user: a pipeline appears containing the policy jobs.

## Checked

2026-10-28. Confirmed against the GitLab pipeline execution policies and scan execution policies pages: skip_ci object with allowed and allowlist.users (id), default ignores skip-ci, pipeline_config_strategy inject_policy, policy jobs always triggered, schedule rules ignore skip_ci, Ultimate tier. Corrected: scan execution policies do not default to allowing skip (the unspecified default ignores it, same as pipeline execution policies). Removed: ci.skip push option, workflow:rules claim, project-link requirement.

Method: documentation only; no commands were run.
