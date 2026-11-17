---
id: computing-software.cloud-infrastructure-engineering.open-policy-agent.ci-pull-request-check-policies
name: ci-pull-request-check-policies
category: computing-software
field: cloud-infrastructure-engineering
product: open-policy-agent
tags: [ci-cd, github-actions, pull-request, changed-files, required-checks]
level: practitioner
status: docs-checked
description: "Use a Rego policy to decide which CI checks run on a pull request from the changed-file list, replacing paths-filter YAML, with a summary job for branch protection."
sources:
  - https://www.openpolicyagent.org/docs/cicd/pr-checks
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
Goal: run only the CI jobs a pull request needs, with logic you can unit test.

The Rego is platform-agnostic; the docs demonstrate it with GitHub Actions, and other CI systems differ only in how changed files are fetched and job outputs are set.

Why Rego rather than the usual approaches:
- `paths-filter` actions are limited to glob patterns, cannot express complex logic and are hard to test in isolation
- shell scripts with `grep` or `find` are fragile and cannot be unit tested
- hard-coded `if:` conditions are duplicated across jobs with no single source of truth

Rego gives testability (`opa test` before it reaches CI), readable declarative rules, reuse across repositories as bundles, and an audit trail because policy changes are versioned and reviewed like code.

The pattern has three parts:
1. A Rego policy that takes the list of changed files as input and outputs which checks should run.
2. A `check-changes` job that evaluates the policy and sets workflow outputs.
3. Conditional jobs that run only when the policy says so.

Optionally a summary job uses OPA to validate that every required job passed, giving branch protection a single required status check.

Example layout: `policy/pr-check/pr_check.rego` beside `pr_check_test.rego`, with `frontend/`, `backend/` and `docs/` directories in the repository and the workflow in `.github/workflows/pull-request.yaml`.

Check: write `pr_check_test.rego` cases for a docs-only change and a backend change, run `opa test policy/ -v`, and confirm the docs-only case selects no code jobs.

## Checked

2026-11-04. Confirmed against the OPA docs page CI/CD, Pull Request Check Policies: the three-part pattern, the comparison with paths-filter, shell scripts and hard-coded if conditions, the benefits list, the example directory layout, the optional summary job for a single required status check, and opa test on the policy directory (the Testing the Policy section runs opa test; the -v flag is shown on the Policy Testing page). Nothing removed.

Method: documentation only; no commands were run.
