---
id: computing-software.devops-ci-cd.gitlab-ci.compute-minutes-quotas-and-cost-factors
name: compute-minutes-quotas-and-cost-factors
category: computing-software
field: devops-ci-cd
product: gitlab-ci
tags: [gitlab-ci, ci-minutes-quota, cost-factor, pipeline-efficiency]
level: practitioner
status: docs-checked
description: "Manage GitLab compute minutes: quota per namespace, cost factors by runner size and project type, usage reports, and cutting consumption before jobs are blocked."
sources: ["https://docs.gitlab.com/ci/pipelines/compute_minutes/", "https://docs.gitlab.com/ci/runners/hosted_runners/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Compute minutes quotas and cost factors

On GitLab.com (and self-managed instance runners if quotas are set), jobs on **instance runners**
consume compute minutes from the top-level namespace quota. Project and group runners you host do
not consume quota.

## Cost factor
Minutes used = job duration (seconds) / 60 x cost factor. Duration excludes time in created or pending status.
- Linux x86-64: small 1, medium 2, large 3, xlarge 6, 2xlarge 12. Linux Arm64: small 1, medium 2, large 3.
- GPU-enabled medium 7; macOS M1 medium 6 and M2 Pro large 12 (both Beta); Windows medium 1 (Beta). Check the compute minutes page for current values.
- Public projects in the GitLab for Open Source program use factor 0.5; their public forks 0.008.
- Trigger jobs use no minutes themselves; the downstream pipeline's jobs do.

## When quota runs out
Once a quota is exceeded, enforcement measures apply to instance-runner jobs (the docs describe the exact behaviour). Free namespaces on GitLab.com get a base monthly quota set by tier; you can buy additional compute minutes, or move jobs to your own runners via `tags:`. Usage resets on the first day of each month.

## Monitoring
- Usage is counted against the job's top-level namespace; the compute minutes page explains where to view it and how self-managed admins enable the quota (the quota is disabled by default on self-managed).

## Reducing consumption
1. Right-size: do not use a large runner size for lint jobs; tag by need.
2. `interruptible: true` + auto-cancel redundant pipelines.
3. `rules:changes` to skip unaffected jobs; avoid duplicate branch + MR pipelines.
4. Cache dependencies and use `needs` to shorten wall clock.
5. Move heavy, long jobs (e2e, builds) to autoscaled group runners on cheaper compute.

## Verify
- [ ] Usage quotas page trend drops after changes; no job lands on large runners without a reason.

## Checked

2026-11-02. Confirmed against the GitLab compute minutes page: usage formula, cost factor table (Linux, Arm64, GPU, macOS, Windows), open-source factors, trigger jobs, monthly reset, quota off by default. Removed: the quoted error message, the exact UI path for usage, the admin setting name, the namespaces API field and the `saas-linux-large` tag name, none of which the fetched pages state.

Method: documentation only; no commands were run.
