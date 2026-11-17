---
id: computing-software.cloud-infrastructure-engineering.terraform.cost-estimation-with-infracost
name: cost-estimation-with-infracost
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, infracost, cost-estimation, finops, cost-diff, pull-request-comments, usage-based-resources, guardrails, cicd, github-actions]
level: practitioner
status: docs-checked
description: "Wire Infracost into Terraform CI so every PR shows the monthly cost delta: breakdown vs diff, baseline handling, GitHub Actions, and Infracost Cloud guardrails."
sources: ["https://github.com/infracost/infracost", "https://github.com/infracost/actions", "https://www.infracost.io/docs/"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost estimation for Terraform with Infracost

**Goal:** every PR that touches infrastructure shows its cost delta as a comment
before anyone reviews the Terraform diff, so cost is part of the review, not a
surprise on next month's bill. (One input to the HCP Terraform run-level cost gate
mentioned in
`computing-software.cloud-infrastructure-engineering.terraform.terraform-cloud-remote-runs-and-vcs-workflows`;
Infracost also works standalone in any CI system.)

## 1. What it covers
Infracost shows cost estimates and FinOps recommendations for Terraform,
Terragrunt, CloudFormation and AWS CDK before changes are deployed, in the terminal,
editor extensions, AI-agent skills and pull requests. The same engine, pricing data
and policies sit behind every entry point. It supports resources on AWS, Azure and
Google Cloud, and can estimate usage-based resources such as S3 and Lambda (see the
"usage based resources" page in the Infracost docs).

The current CLI starts with `infracost setup` (authentication, editor, agent skills,
CI wiring) and `infracost scan`; `infracost inspect` gives resource-level breakdowns
and policy details. The older `breakdown` / `diff` / `comment` commands still
appear in the legacy GitHub Actions flow below.

## 2. Pull-request comments with GitHub Actions
The Infracost GitHub App is recommended where your organisation allows it; the
actions are the alternative.
- `infracost/actions/diff` computes the cost difference between a base checkout and
  a head checkout, posts a PR comment, and marks the PR merged or closed in the
  Infracost dashboard when it ends.
- `infracost/actions/scan` scans one directory and uploads baseline cost data; run it
  on pushes to the default branch.
- Both need an `api-key` (store as a secret) and run the `ghcr.io/infracost/ci`
  image, so the runner needs Docker. The job needs `pull-requests: write`.

The legacy `infracost/actions/setup` flow runs the commands yourself:
```bash
infracost breakdown --path=. --format=json --out-file=infracost-base.json   # on the base branch
infracost diff --path=. --format=json --compare-to=infracost-base.json --out-file=infracost.json   # on the PR branch
infracost comment github --path=infracost.json --repo=$GITHUB_REPOSITORY \
  --github-token=$TOKEN --pull-request=$PR_NUMBER --behavior=update
```
`diff --compare-to` needs a baseline from the base branch; `--behavior=update`
updates the existing comment instead of adding a new one per push.

## 3. Policy
Infracost Cloud lets leads define tagging policies and guardrails once and have
them enforced across CLI, editor, agent skills and CI. Start advisory (comment
only) before blocking merges, and keep an override path for intended large changes.

## Gotchas
- A baseline generated from a stale base branch makes the delta compare against old
  state; regenerate it from the current base on each run.
- Usage-based resources need usage assumptions; check the breakdown for resources
  with missing usage data before trusting a total.
- Tag-based cost allocation needs consistent tagging in your own code; Infracost
  does not enforce it unless you configure tagging policies in Infracost Cloud.

## Verify
- [ ] Every infra PR gets an automatic cost-delta comment before review.
- [ ] The comparison baseline comes from the current base branch.
- [ ] Any cost policy started advisory before becoming blocking.

## Checked
2026-11-09. Confirmed against the infracost/infracost README (supported IaC, `infracost setup`, `infracost scan`, `infracost inspect`, over 1,100 resources on AWS/Azure/Google, usage-based resources, Infracost Cloud tagging policies and guardrails) and the infracost/actions README (diff, scan, legacy setup flow, `breakdown`, `diff --compare-to`, `comment github` flags, `--behavior=update`, Docker requirement).
Removed as unconfirmed: the `infracost-usage.yml` schema and Lambda field names, `generate-usage-estimates`, `--terraform-plan-flags` / `--terraform-plan-file` advice, the claim that prices are list prices that exclude discounts, the "silently defaults to $0" claim, pricing-coverage statements, and a dollar example.
Method: documentation only; no commands were run.
