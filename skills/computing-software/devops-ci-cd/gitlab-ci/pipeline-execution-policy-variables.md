---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-execution-policy-variables
name: pipeline-execution-policy-variables
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, policy-variables-override, pipeline-execution-policy, variable-precedence]
level: advanced
status: docs-checked
description: "Control how project CI variables interact with pipeline execution policy jobs: precedence, variables_override allowlists, and keeping enforced jobs tamper-proof."
sources: ["https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/", "https://docs.gitlab.com/ci/variables/#cicd-variable-precedence"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Policy variable precedence and enforced variables

Policy jobs run inside the project pipeline. By default the policy variables are enforced with the highest precedence and users cannot override them (for example `SAST_DISABLED` or `CS_IMAGE` set in project settings do not change policy jobs). `variables_override` loosens this on purpose.

## variables_override (introduced in GitLab 18.1)
```yaml
pipeline_execution_policy:
  - name: Enforced scanning
    pipeline_config_strategy: inject_policy
    content: { include: [{ project: sec/policies, file: scan.yml }] }
    variables_override:
      allowed: false            # deny user-defined overrides...
      exceptions:               # ...except these
        - CS_IMAGE
        - SAST_EXCLUDED_PATHS
```
`allowed: true` + `exceptions` = denylist mode instead.

## Precedence reminder (highest first)
Variables defined in a pipeline execution policy or a scan execution policy sit at the top of GitLab's CI/CD variable precedence order; see the CI/CD variable precedence page for the full list.

## Hardening
- Hard-code security-relevant variables at job level in the policy YAML.
- Set the project setting "Minimum role to use pipeline variables" to `no_one_allowed`, so no pipeline can run with pipeline variables.
- Only include policy CI files from a repository you control.

## Verify
- [ ] Set `SAST_DISABLED=true` in project variables; the policy SAST job still runs.

## Checked

2026-10-28. Confirmed on the pipeline execution policies and CI/CD variables pages: policy variables enforced with the highest precedence by default, variables_override with allowed and exceptions (allowlist when allowed is false, denylist when true), introduced in 18.1, the dotenv option, precedence list starting with policy variables, the Minimum role to use pipeline variables setting with no_one_allowed. Removed: SECURE_ANALYZERS_PREFIX, the wrong claim that project variables override policy variables by default, and the incorrect full precedence chain.
Method: documentation only; no commands were run.
