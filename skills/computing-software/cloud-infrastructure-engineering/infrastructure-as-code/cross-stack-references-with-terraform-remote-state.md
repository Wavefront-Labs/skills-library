---
id: computing-software.cloud-infrastructure-engineering.infrastructure-as-code.cross-stack-references-with-terraform-remote-state
name: cross-stack-references-with-terraform-remote-state
category: computing-software
field: cloud-infrastructure-engineering
product: infrastructure-as-code
tags: [infrastructure-as-code, state-management, terraform-remote-state, remote-state, state-isolation]
level: practitioner
status: docs-checked
description: "Share outputs between Terraform stacks with terraform_remote_state or explicitly published data, and know when to use tfe_outputs."
sources:
  - https://developer.hashicorp.com/terraform/language/state/remote-state-data
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Cross-stack references

Splitting state per stack (network, data, app) needs a way for app to read network's IDs.

## terraform_remote_state
```hcl
data "terraform_remote_state" "vpc" {
  backend = "local"
  config = {
    path = "..."
  }
}

resource "aws_instance" "foo" {
  subnet_id = data.terraform_remote_state.vpc.outputs.subnet_id
}
```
- The data source reads the latest state snapshot from the named backend and exposes only that configuration's **root module outputs** (`outputs` attribute). Resource data and nested-module outputs are not accessible; pass a nested module output through an `output` block in the root module.
- Arguments: `backend` (required), `workspace` (optional), `config` (the backend's own arguments; nested blocks become object attributes), `defaults` (values used if the state is empty or lacks an output).
- It needs no provider configuration; it comes from a built-in provider.

## Security trade-off
The reader needs access to the entire state snapshot, which often holds sensitive data. Anyone able to read the root outputs can read the full snapshot by direct requests. HashiCorp says not to use `terraform_remote_state` if any resource in the configuration works with data you consider sensitive.

## Alternatives
- Publish data explicitly to a separate store with its own access controls, then read it with the matching data source. Documented pairs include Route 53 and other DNS records (read by normal DNS lookups or the `dns` provider), S3 objects, SSM Parameter Store, Azure Automation variables, Google Cloud Storage objects, Consul key/value, Kubernetes config maps.
- Generic blob stores can hold structured data via `jsonencode` and `jsondecode`.
- A data-only module can hide the retrieval details so the strategy can change later.
- A shared store other systems can read (DNS, Consul, config maps) can also serve non-Terraform consumers.
- On HCP Terraform or Terraform Enterprise, use the `tfe_outputs` data source instead: it is recommended as more secure because it does not need full access to workspace state.

## Verify
- [ ] Reader credentials are scoped to what the dependency needs.
- [ ] Every cross-stack value comes from a root output or a published store entry, not a hardcoded ID.

## Checked
Method: docs-checked 2026-11-09 against the HashiCorp "terraform_remote_state data source" page (full text read).
Removed: S3 backend example values, comparison table pros and cons, output-as-API hygiene advice, circular-reference and plan-time gotchas, terraform console check, tfe_outputs registry page (unread).
