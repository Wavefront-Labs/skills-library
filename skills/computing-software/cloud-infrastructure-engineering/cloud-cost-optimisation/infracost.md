---
id: computing-software.cloud-infrastructure-engineering.cloud-cost-optimisation.infracost
name: infracost
category: computing-software
field: cloud-infrastructure-engineering
product: cloud-cost-optimisation
tags: [cloud-cost-optimisation, finops, cost-estimation, infracost, iac-cost-estimation, pull-request-cost, terraform-cost, shift-left-finops, usage-file, cost-policies]
level: practitioner
status: docs-checked
description: "Show the cost impact of Terraform changes in pull requests with Infracost: CI setup, usage files for usage-based resources, diff output, thresholds/policies and its limits."
sources: ["https://www.infracost.io/docs/", "https://www.infracost.io/docs/features/usage_based_resources/", "https://github.com/infracost/actions"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Cost estimates in pull requests (Infracost)

Infracost reads Terraform, CloudFormation and AWS CDK code and shows cost estimates, FinOps policy violations and tagging
issues in the editor and in pull requests, for AWS, Azure and Google Cloud. The CLI and its commands change between
releases, so follow the current docs and the Actions README rather than copying old pipelines.

## Setup
1. Get an API key (the docs describe a free key) and store it as the CI secret `INFRACOST_API_KEY`.
2. GitHub Actions: `infracost/actions/setup` installs the CLI with `api-key`. You then run `infracost breakdown`,
   `infracost diff` and `infracost comment` as separate steps; the Actions README says new integrations should prefer
   `diff` and `scan`.
3. Baseline pattern: run `infracost breakdown --path=.` with JSON output on the base branch, then on the PR branch
   compare with `--compare-to=<base json>`, then post with `infracost comment github --path=<json>`.

## Usage-based resources
Costs that depend on usage (requests, GB stored or transferred) cannot be read from code.
- Infracost predefines values that set each usage-based cost to a small placeholder so these resources are not shown as
  free; you can see and change them under Org Settings > Usage defaults.
- Disabling the predefined values means usage keys you have not overridden show no cost, and engineers may think the
  resources are free.
- Teams can supply their own `infracost-usage.yml` in the repo; its values are merged with the central ones and take
  precedence. Reference it from `infracost.yml` with `usage_file` at top level or per project.

## Making it useful
1. Teach reviewers to read the monthly delta and ask whether it is expected.
2. Set usage values for the top usage-based resources so the delta is not understated.
3. Decide a policy for when a cost increase needs approval; configure it in Infracost Cloud per its docs.

## Verify
- [ ] A PR adding an instance shows a cost delta.
- [ ] Usage file reviewed for the top usage-based resources.

## Checked
2026-11-01. Confirmed in the Infracost docs home (supported IaC, clouds, policy and tagging checks, free API key), the
usage-based resources page (predefined placeholder values, Usage defaults, `infracost-usage.yml`, `usage_file` in
`infracost.yml`) and the Actions README (`api-key`, separate breakdown/diff/comment steps, `--compare-to`, prefer
diff and scan). Removed: `--sync-usage-file`, the "$0 unless you provide a usage file" claim (docs now describe predefined
values), threshold and OPA guardrail claims, Terragrunt/Pulumi support claims and the price-list limits claim.
Method: documentation only; no commands were run.
