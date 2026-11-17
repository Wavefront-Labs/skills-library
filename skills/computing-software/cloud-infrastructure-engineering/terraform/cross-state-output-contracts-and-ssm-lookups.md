---
id: computing-software.cloud-infrastructure-engineering.terraform.cross-state-output-contracts-and-ssm-lookups
name: cross-state-output-contracts-and-ssm-lookups
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, remote-state-outputs, output-contract, data-source-lookup, ssm-parameter-lookup, cross-state, layered-states]
level: advanced
status: docs-checked
description: "Treat root outputs as a versioned contract between states, and replace terraform_remote_state with tag-based data lookups or SSM/parameter-store publishing."
sources: ["https://developer.hashicorp.com/terraform/language/state/remote-state-data#alternative-ways-to-share-data-between-configurations", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/ssm_parameter.html.markdown", "https://raw.githubusercontent.com/hashicorp/terraform-provider-aws/main/website/docs/d/vpc.html.markdown", "https://developer.hashicorp.com/terraform/language/values/outputs"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Sharing data between states

## Outputs as a contract
When `app` reads `network`'s outputs, those outputs are an API:
```hcl
# network/outputs.tf
output "vpc_id"             { value = aws_vpc.main.id }
output "private_subnet_ids" {
  description = "Map of AZ => subnet ID. Stable keys; consumers iterate."
  value       = { for k, s in aws_subnet.private : k => s.id }
}
```
Rules:
- Never rename/remove an output without a deprecation window: add the new one, migrate
  consumers, then delete.
- Prefer maps with stable keys over lists (index shifts break consumers).
- Output IDs, not whole objects (design guidance: whole objects couple consumers to
  provider schema changes); mark secrets `sensitive = true`, which redacts them in CLI output.
- Give every output a `description`.

## Why move off `terraform_remote_state`
HashiCorp's docs: it only exposes output values, but its user must have access to the
entire state snapshot, which often includes sensitive information. HashiCorp recommends,
when possible, publishing data explicitly to a separate location so shared information and
state snapshots can have different access controls. That store can also be read by systems
other than Terraform.

## Alternative 1: look things up by tag
```hcl
data "aws_vpc" "main" {
  tags = { "acme:layer" = "network", "acme:env" = var.env }
}
data "aws_subnets" "private" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.main.id]
  }
  tags = { "acme:tier" = "private" }
}
```
Zero coupling to state; works for resources made outside Terraform. The `tags` map
must exactly match a pair on the desired object (`aws_vpc`, `aws_subnets`); `aws_subnets`
returns a set of IDs, `aws_vpc` a single VPC.

## Alternative 2: publish to a parameter store
```hcl
# producer
resource "aws_ssm_parameter" "vpc_id" {
  name  = "/platform/${var.env}/network/vpc_id"
  type  = "String"
  value = aws_vpc.main.id
}
# consumer
data "aws_ssm_parameter" "vpc_id" {
  name = "/platform/${var.env}/network/vpc_id"
}
```
The `aws_ssm_parameter` data source marks `value` as sensitive in plan output regardless of
type, but a SecureString's unencrypted value is stored in raw state as plain text, so state
access still matters. Other publish/read pairs HashiCorp lists: `aws_s3_object`,
`azurerm_automation_variable_string`, `google_storage_bucket_object`, `consul_key_prefix`,
`kubernetes_config_map`, DNS records, and `tfe_outputs` for HCP Terraform.

## Choosing
| Need | Pick |
|---|---|
| Same team, same backend, no secrets in state | `terraform_remote_state` is fine |
| Many consumers, least privilege | parameter store |
| Resources may be created outside Terraform | tag lookup |
| HCP Terraform | `tfe_outputs` (recommended by HashiCorp: does not require full workspace state access) |

## Verify
- [ ] Consumer plan works with only the parameter-path / tag-read permissions.
- [ ] Renaming an output in the producer is caught by a consumer plan in CI before merge.

## Checked
2026-11-08. Confirmed against the Terraform remote-state data source page (full-state access drawback, explicit publishing recommendation, publish/read pairs, tfe_outputs), the outputs page (description, sensitive), and the AWS provider docs for aws_vpc, aws_subnets and aws_ssm_parameter (tags matching, sensitive value, SecureString plain text in state; the registry pages are empty stubs so the provider repo docs were read). Removed: terraform-docs, the claim that remote state fails before the producer applies, the singular-lookup error claim, and Azure App Configuration / Key Vault, GCP Secret Manager and Runtime Config equivalents (not documented there). The output-contract rules are design guidance.
Method: documentation only; no commands were run.
