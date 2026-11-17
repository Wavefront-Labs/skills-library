---
id: computing-software.cloud-infrastructure-engineering.terraform.parallelism-and-provider-api-throttling
name: parallelism-and-provider-api-throttling
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, parallelism-flag, api-throttling, retry-mode, max-retries, rate-limiting, performance]
level: advanced
status: docs-checked
description: "Tune -parallelism and provider retry settings (AWS max_retries/retry_mode, Azure/GCP equivalents) to fix throttling errors and slow plans on large states."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/plan#parallelism-n", "https://developer.hashicorp.com/terraform/internals/graph", "https://developer.hashicorp.com/terraform/cloud-docs/variables", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs#retry_mode", "https://registry.terraform.io/providers/hashicorp/google/latest/docs/guides/provider_reference#request_timeout"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `-parallelism` and API throttling

## -parallelism
Limits concurrent graph-walk operations (refresh, create, update, destroy). Default 10.
```bash
terraform plan  -parallelism=30     # large, read-heavy refresh on a generous API
terraform apply -parallelism=4      # strict rate limits / fragile APIs
export TF_CLI_ARGS_plan="-parallelism=20"
```
- Higher speeds up refresh of thousands of resources until the API throttles.
- It limits graph nodes processed concurrently by one Terraform process (graph docs: default 10, flag on plan, apply and destroy).
- HashiCorp calls it an advanced setting, "helpful in certain special use cases or to help debug"; Terraform does not use it to address API rate limits directly, because providers such as AWS back off and retry in their API clients.
- HCP Terraform: set `TFE_PARALLELISM` env var on the workspace.

## Throttling symptoms
Provider errors that mention throttling, rate limits or HTTP 429. The AWS provider
retries throttled calls (see `max_retries`), so failures appear when retries run out.

## Provider retry settings
```hcl
provider "aws" {
  region      = "eu-west-1"
  max_retries = 25            # default 25; the delay between retries grows exponentially
  retry_mode  = "adaptive"    # valid values: standard, adaptive
}
```
`AWS_MAX_ATTEMPTS` and `AWS_RETRY_MODE` env vars also apply. Google provider:
`request_timeout` limits a single HTTP request (default 120s); the `batching` block
(`send_after`, `enable_batching`) is implemented for only a few resources, and the
provider docs advise avoiding custom batching unless you know what you are doing.
AzureRM: lower `-parallelism`.

## Structural fixes
- Split huge states: plan time and API calls scale with resource count.
- `-refresh=false` for quick iterative plans when you know nothing drifted (never for the final apply plan).
- Fewer data sources: each is an API call on every plan.
- Avoid many tiny resources where the provider offers a bulk resource.

## Gotchas
- `-parallelism=1` is a debugging aid, not a fix.
- Retry storms across many concurrent pipelines share the same account limits —
  stagger schedules.

## Verify
- [ ] Plan duration and throttling counts (`TF_LOG=DEBUG ... | grep -c Throttl`) before/after tuning.
- [ ] No throttling failures across three consecutive full plans.

## Checked
- 2026-10-28. Confirmed against the Terraform `plan` command page and the "Dependency Graph" page (`-parallelism=n`, default 10, plan/apply/destroy, advanced option, providers handle rate limits), the AWS provider docs (`max_retries` default 25 with exponential delay, `retry_mode` values `standard` and `adaptive`, `AWS_MAX_ATTEMPTS`, `AWS_RETRY_MODE`), the Google provider reference (`request_timeout` default 120s, `batching` with `send_after` and `enable_batching`), the HCP Terraform variables page (`TFE_PARALLELISM`) and `TF_CLI_ARGS_name` on the CLI environment-variables page.
- Removed: named error strings (ThrottlingException, TooManyRequests and similar), the claim that `standard` is the default retry mode, per-provider mutex claim and Azure per-hour limits (not in the fetched docs).
Method: documentation only; no commands were run.
