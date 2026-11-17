---
id: computing-software.devops-ci-cd.ci-pipeline-design.ci-cost-attribution
name: ci-cost-attribution
category: computing-software
field: devops-ci-cd
product: ci-pipeline-design
tags: [ci-pipeline-design, ci-cost-attribution, pipeline-observability, actions-cost]
level: practitioner
status: docs-checked
description: "Understand how GitHub Actions and GitLab bill CI usage (per-minute SKUs, cost factors, who is charged) so spend can be attributed and reduced."
sources: ["https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions", "https://docs.gitlab.com/ci/pipelines/compute_minutes/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# CI cost attribution per pipeline

Attribution starts with knowing how the platform meters usage.

## GitHub Actions billing
- Usage on private and internal repositories draws from a monthly included compute amount
  expressed as money, not minutes; beyond it, usage is billed. Usage is charged to the
  **repository owner**, not whoever triggered the run. Standard GitHub-hosted runners on
  public repositories and self-hosted runners are free and do not draw on the included amount;
  larger runners are billed even for public repositories.
- Each runner type has a per-minute rate set by operating system and size, tracked by billing
  SKU. Rates on the page: Linux 1-core `actions_linux_slim` $0.002, Linux 2-core `actions_linux`
  $0.006, Linux 2-core arm64 `actions_linux_arm` $0.005, Windows 2-core `actions_windows`
  $0.010, macOS 3/4-core `actions_macos` $0.062. Rates change, so re-check the page.
- A 10-minute job on a standard Linux runner costs $0.06 (10 x $0.006). A job that fails after
  5 minutes and is re-run for 10 costs 15 minutes: failed and re-run attempts both bill.
- Artifact and cache storage are billed separately (cache: 10 GB included per repository,
  measured by hourly peak).
- The billing dashboard may show spend as a dollar amount rather than minutes.

## GitLab compute minutes
- Job usage = `job duration (seconds) / 60 x cost factor`, added to the **top-level namespace**
  of the project, not the user who ran the pipeline. Time in `created` or `pending` is excluded.
- The cost factor is a multiplier, not a price. Linux x86-64 `small` is 1, `medium` 2, `large`
  3, `xlarge` 6, `2xlarge` 12; macOS M1 medium 6 and M2 Pro large 12 (both Beta).
- Concurrent jobs mean pipeline compute can exceed pipeline wall-clock time. Trigger jobs do
  not use runners and cost nothing; the downstream pipeline they start does.
- Usage resets on the first day of each month; the quota is shown in the instance runner
  usage dashboard.

## Reporting (judgement, not from the sources)
Group by repository or namespace, then map each to an owning team. List the top jobs by cost
with an owner.

## Reducing usage (GitLab page)
Disable pipelines for project mirror updates, reduce scheduled pipeline frequency, skip
pipelines when not needed, use `interruptible` jobs that auto-cancel when a new pipeline
starts, use `rules` so jobs only run when needed, and use private runners for some jobs.

## Verify
- [ ] Every repository or namespace that incurs spend maps to a named owner.
- [ ] Top-cost jobs have an owner and a reduction target.

## Checked
Confirmed 2026-11-09 against the GitHub Actions billing page (read the compute, SKU, example and storage sections) and the GitLab compute minutes page (formula, cost factors, reset, reduction list), from local text copies.
Removed as unconfirmed: the billing usage API endpoint, CSV usage report steps, CODEOWNERS mapping, AWS/GCP cost allocation tags, Kubecost/OpenCost, ARC pod-label advice, the per-job cost formula for self-hosted fleets, OpenTelemetry cost export, and the spot/preemptible, path-filter and caching savings list.
Method: docs-checked 2026-11-09 against docs.github.com about billing for GitHub Actions and docs.gitlab.com compute minutes
