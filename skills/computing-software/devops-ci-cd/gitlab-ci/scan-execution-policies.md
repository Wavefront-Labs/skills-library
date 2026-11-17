---
id: computing-software.devops-ci-cd.gitlab-ci.scan-execution-policies
name: scan-execution-policies
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, scan-execution-policy, enforced-security-scans, scheduled-security-scans, security-policy-project]
level: advanced
status: docs-checked
description: "Force SAST, secret detection, dependency and container scanning on projects with scan execution policies, triggered by pipelines or schedules, without editing project CI files."
sources: ["https://docs.gitlab.com/user/application_security/policies/scan_execution_policies/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Scan execution policies (Ultimate)

## 1. Policy YAML (security policy project)
```yaml
scan_execution_policy:
  - name: Baseline scans
    description: SAST + secrets on every branch pipeline, container scan nightly
    enabled: true
    rules:
      - type: pipeline
        branch_type: all              # all | default | protected | target_default...
      - type: schedule
        branches: [main]
        cadence: "0 3 * * *"          # cron; add timezone (IANA name) if needed
    actions:
      - scan: sast
      - scan: secret_detection
      - scan: dependency_scanning
      - scan: container_scanning
        variables: { CS_IMAGE: "$CI_REGISTRY_IMAGE:latest" }
    policy_scope:
      projects: { excluding: [{ id: 101 }] }
```
Edit in the policy editor (it opens a merge request against the security policy project) or directly in the policy YAML.

## 2. Behaviour
- `pipeline` rules add scan jobs to project pipelines; `schedule` rules run scans on a cadence even when no pipeline is created.
- Scans use the default or latest GitLab security CI/CD templates; `variables` in the action set CI/CD variables for that scan.

## 3. Versus pipeline execution policies
Scan execution = only GitLab security scanners, minimal config. Pipeline execution = arbitrary
jobs (your own scanners, compliance checks). Combine with **merge request approval policies** to
make findings block merges.

## Gotchas
- Container scanning needs `CS_IMAGE` resolvable in every project — use variables per scope or limit to projects that build images.
- Scheduled scans on many projects spike runner load at the same minute — stagger cadences or use `time_window` where available.
- Policy jobs run on runners matching the action's `tags` list, if you set one.

## Verify
- [ ] A project without security templates shows `sast`/`secret_detection` jobs labelled as policy jobs.

## Checked

2026-10-28. Confirmed on the scan execution policies page: Ultimate tier, rules of type pipeline and schedule, branch_type values (default, protected, all, target_default, target_protected), cadence cron, timezone as IANA identifier, time_window, policy_scope, scan actions with variables and tags, policy editor opens a merge request to the security policy project, schedule scans run even without pipelines. Removed: UTC default, Secure > Policies path, bot user, project-variable and non-removable-job claims, injected-pipeline-for-projects-without-CI claim.
Method: documentation only; no commands were run.
