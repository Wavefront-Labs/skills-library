---
id: computing-software.devops-ci-cd.gitlab-ci.migrating-compliance-pipelines-to-execution-policies
name: migrating-compliance-pipelines-to-execution-policies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, compliance-pipeline-migration, compliance-pipelines, pipeline-execution-policy]
level: advanced
status: docs-checked
description: "Migrate deprecated GitLab compliance pipelines (framework pipeline configuration) to pipeline execution policies scoped by compliance framework, with a parallel-run plan."
sources: ["https://docs.gitlab.com/user/compliance/compliance_pipelines/", "https://docs.gitlab.com/user/application_security/policies/pipeline_execution_policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Migrating compliance pipelines to pipeline execution policies

Compliance pipelines (the "Compliance pipeline configuration" field on a compliance framework) are
deprecated in 17.3 and planned for removal in 20.0. Replacement: pipeline execution policies scoped to the framework.

## Mapping
| Compliance pipeline | Pipeline execution policy |
|---|---|
| The framework's compliance pipeline configuration file | `content.include` of the same file |
| Must `include` the project's `.gitlab-ci.yml` manually | `inject_policy` merges automatically; `override_project_ci` replaces it |
| Applies to projects with the framework label | `policy_scope: { compliance_frameworks: [{ id: N }] }` |
| Runs in project context | same, plus reserved stages `.pipeline-policy-pre/.pipeline-policy-post` |

## Steps
1. Create/link a security policy project to the top-level group.
2. Write the policy:
   ```yaml
   pipeline_execution_policy:
     - name: SOX controls
       enabled: true
       pipeline_config_strategy: override_project_ci   # same semantics as old compliance pipelines
       content: { include: [{ project: compliance/ci, file: sox.yml }] }
       policy_scope: { compliance_frameworks: [{ id: 7 }] }
   ```
3. Remove the manual `include: project: $CI_PROJECT_PATH file: .gitlab-ci.yml` from the old file
   when switching to `inject_policy`; otherwise jobs duplicate.
4. Do not run both on the same project: the docs warn that compliance pipelines and pipeline execution policies together can duplicate jobs, fail pipelines or skip checks. Pilot on a separate group, compare job lists, then clear the framework's pipeline config.

## Gotchas
- Job name clashes get a unique suffix by default (`suffix: on_conflict`); `suffix: never` fails the pipeline instead.
- Needs Ultimate.

## Verify
- [ ] A framework-labelled project shows policy jobs; an unlabelled one does not.

## Checked

2026-10-28. Confirmed on the compliance pipelines and pipeline execution policies pages: compliance pipelines deprecated in 17.3 and planned for removal in 20.0 (not 19.0 as the draft said), Ultimate tier, inject_policy and override_project_ci strategies, policy_scope by compliance framework, suffix on_conflict (default) or never, warning not to enable execution policies until compliance pipelines are migrated. Removed: the Migrate pipeline to policy action, the pipeline_configuration_full_path field name, the run-both pilot step, and the CI_PROJECT_PATH note.
Method: documentation only; no commands were run.
