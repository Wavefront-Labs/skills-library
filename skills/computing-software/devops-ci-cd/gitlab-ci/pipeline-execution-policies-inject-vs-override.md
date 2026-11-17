---
id: computing-software.devops-ci-cd.gitlab-ci.pipeline-execution-policies-inject-vs-override
name: pipeline-execution-policies-inject-vs-override
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, inject-ci, inject-policy, override-project-ci, pipeline-execution-policy, policy-reserved-stages]
level: advanced
status: docs-checked
description: "Enforce CI jobs across projects with pipeline execution policies: inject_policy/inject_ci vs override_project_ci strategies, reserved stages, scoping and failure modes."
sources: ["https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Pipeline execution policy: inject vs override (Ultimate)

Defined in the **security policy project** (`.gitlab/security-policies/policy.yml`) linked to a group/project.

## 1. Policy
```yaml
pipeline_execution_policy:
  - name: Mandatory checks
    description: SBOM and license gate on every pipeline
    enabled: true
    pipeline_config_strategy: inject_policy        # or override_project_ci
    content:
      include:
        - project: compliance/pipeline-policies
          file: mandatory.yml
          ref: v2.1.0
    policy_scope:
      compliance_frameworks: [{ id: 7 }]
```

## 2. Strategies
- **inject_policy** (successor of `inject_ci`): policy jobs are merged into the project pipeline.
  Policy jobs can use the reserved stages `.pipeline-policy-pre` (runs before everything, failure
  stops the pipeline) and `.pipeline-policy-post` (always last), or project stages if they exist
  (`inject_policy` can inject custom stages too). Job name collisions get a suffix instead of overwriting.
- **inject_ci** (deprecated): use `inject_policy` for new policies.
- **override_project_ci**: the policy config **replaces** the project's `.gitlab-ci.yml`. To keep
  project jobs, the policy must `include: { project: $CI_PROJECT_PATH, ref: $CI_COMMIT_SHA, file: $CI_CONFIG_PATH }`.

## 3. What projects cannot do
- The skip-ci directive is ignored for pipelines with policies by default; the policy's `skip_ci` setting can allow chosen users.
- Policy variables have the highest precedence unless `variables_override` allows overrides.
- Policies stay in effect even if the project has no CI/CD configuration file.

## 4. Gotchas
- Users who trigger pipelines need at least read access to the project holding the policy's CI file, otherwise pipelines do not start.
- `.pipeline-policy-pre` jobs delay every pipeline — keep them seconds long.
- A security policy project applies at most five pipeline execution policies; any after the first five are ignored.

## Verify
- [ ] Project pipeline graph shows `.pipeline-policy-pre` jobs; removing them from `.gitlab-ci.yml` has no effect.

## Checked

2026-10-28. Confirmed on the pipeline execution policies page: Ultimate tier, pipeline_config_strategy values inject_policy, inject_ci (deprecated), override_project_ci, reserved stages .pipeline-policy-pre (before .pre) and .pipeline-policy-post (after .post), suffix on_conflict (default) vs never, the override_project_ci include of $CI_PROJECT_PATH/$CI_COMMIT_SHA/$CI_CONFIG_PATH, policy_scope with compliance_frameworks, skip_ci behaviour, five-policy limit, read access to the policy CI file. Removed: skip_projects, the job token allowlist claim, and the claim that policy jobs cannot be skipped with rules. The ref v2.1.0 in the example is a placeholder.
Method: documentation only; no commands were run.
