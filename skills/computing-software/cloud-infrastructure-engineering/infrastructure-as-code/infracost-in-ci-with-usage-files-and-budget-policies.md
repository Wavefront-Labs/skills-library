---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.infracost-in-ci-with-usage-files-and-budget-policies
name: infracost-in-ci-with-usage-files-and-budget-policies
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, iac-cost, infracost, infracost-ci, cost-diff-comment, usage-file, infracost-usage, cost-policy, budget-gate]
level: practitioner
status: docs-checked
description: "Add Infracost cost estimates to pull requests and model usage-based costs with infracost-usage.yml and per-project usage files."
sources:
  - https://www.infracost.io/docs/integrations/cicd/
  - https://www.infracost.io/docs/features/usage_based_resources/
licence: Apache-2.0
version: 4
updated: 2026-11-17
---

# Infracost in CI with usage files

## Pull request integration
Infracost has direct integrations for GitHub, Azure Repos and GitLab, which its docs recommend as simpler and faster to set up. Other CI systems (TeamCity, CodeBuild, Harness, Buildkite, anything that can run a container) follow the "any CI/CD system" guide. Those guides use the `ghcr.io/infracost/ci` image, which ships git and the infrastructure code parsers; tags are `latest`, a major series (`2`, the one the docs say to use), a minor series and an exact version (only the exact version is immutable). Follow the current integration guide for the exact commands, because the CLI flow has changed across versions.

## Baseline versus usage costs
- Baseline costs are fixed charges for provisioned resources, such as the hourly cost of a VM; Infracost assumes the whole month (730 hours).
- Usage costs depend on actual usage, such as object-storage volume. Infracost estimates them from usage defaults in Infracost Cloud (paid) or from `infracost-usage.yml` at the root of the repo (free). In output, costs marked with `*` are usage costs.
- Repo-level values are merged with centrally defined values and take precedence.
- The predefined values aim at about $5/month per usage-based cost for common configurations so that engineers do not treat these resources as free. Disabling predefined values means unset usage keys show no cost, which can make resources look free.

## Referencing usage files
Set `usage_file` in `infracost.yml`, either at the top level for all projects or per project (current docs show `version: "0.3"`):
```yaml
version: "0.3"
projects:
  - path: dev
    usage_file: dev-usage.yml
  - path: prod
    usage_file: prod-usage.yml
```

## Usage file shape
```yaml
version: 0.1
resource_type_default_usage:
  aws_dynamodb_table:
    storage_gb: 1000
resource_usage:
  aws_dynamodb_table.my_table:
    monthly_write_request_units: 200
  module.my_module.aws_dynamodb_table.my_table:
    storage_gb: 1000
```
- `resource_type_default_usage` applies to every resource of that type; `resource_usage` applies to named resources and merges with the defaults. Use the full module path (as in Infracost's Name column) for module resources.
- The usage file does not support project filters; per-project values need separate files. Infracost Cloud overrides can filter by project.
- Use `[*]` for resources with `count` or `for_each`; a specific index or key overrides the wildcard.
- EC2 what-if analysis of Reserved Instances is possible through usage keys (`reserved_instance_type`, `reserved_instance_term`, `reserved_instance_payment_option`).

## Checked
Method: docs-checked 2026-11-09 against the Infracost "CI/CD integrations" index page and "Usage-based resources" page (full text read).
Removed: GitHub Actions workflow, breakdown/diff/comment commands, sync-usage-file generator, jq budget gate and Cloud guardrail claims, list-price/private-registry/plan-JSON gotchas (not confirmed on pages read; the config-file page was only searched, not fully read).
