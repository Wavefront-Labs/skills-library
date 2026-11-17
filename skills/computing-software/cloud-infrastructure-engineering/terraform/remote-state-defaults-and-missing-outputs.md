---
id: computing-software.cloud-infrastructure-engineering.terraform.remote-state-defaults-and-missing-outputs
name: remote-state-defaults-and-missing-outputs
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, remote-state-defaults, terraform-remote-state, outputs, cross-stack]
level: practitioner
status: docs-checked
description: "Use the defaults argument of terraform_remote_state when state is empty or lacks an output, know its root-outputs-only limit, and when try() or a separate store fits better."
sources: ["https://developer.hashicorp.com/terraform/language/state/remote-state-data", "https://developer.hashicorp.com/terraform/language/functions/try"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform_remote_state` defaults and missing outputs

## What the data source does
It reads the latest state snapshot from a state backend and exposes the root module
output values of another configuration as the `outputs` attribute (Terraform 0.12+).
It needs no provider configuration; it comes from the built-in provider
`terraform.io/builtin/terraform`.

Arguments: `backend` (required), `workspace` (optional, if the backend supports
workspaces), `config` (optional object; any argument valid in the equivalent
`terraform { backend "<TYPE>" { ... } }` block; nested blocks become object attributes,
for example `workspaces = { ... }`), and `defaults`.

## `defaults`
`defaults` (optional object): default values for outputs "in case the state file is
empty or lacks a required output".
```hcl
data "terraform_remote_state" "vpc" {
  backend = "local"
  config = {
    path = "..."
  }
  defaults = {
    subnet_id = null
  }
}
```
Use it deliberately where downstream must still evaluate when upstream has not been
applied or does not publish an output. For a required value a placeholder only moves the
failure elsewhere, so leave it out and let the missing output surface.

## Only root outputs are visible
Only root-level outputs of the remote state are exposed; resource data and nested module
outputs are not. To expose a nested module value, add a passthrough in the upstream root
module:
```hcl
output "app_value" {
  value = module.app.example
}
```
Without that `output` block the data is not reachable through `terraform_remote_state`.

## `try()` for an output that may be absent
`try` returns the result of the first argument expression that does not produce an
error, so it can fall back when an attribute is absent:
```hcl
try(data.terraform_remote_state.vpc.outputs.new_name, data.terraform_remote_state.vpc.outputs.old_name)
```
HashiCorp suggests using `try` only in local values that normalise data, and only with
simple attribute references and type conversions, because overuse makes configuration
hard to maintain. It catches only dynamic errors; it does not catch provably invalid
constructs such as a reference to an undeclared local value.

## Security and alternatives
- Anyone who can read the output values can also read the full state snapshot by direct
  network requests. Do not use `terraform_remote_state` if resources in your configuration
  work with data you consider sensitive.
- For HCP Terraform or Terraform Enterprise, HashiCorp recommends the `tfe_outputs`
  data source of the HCP Terraform/Enterprise provider, which does not require full state
  access.
- Where possible, publish shared data explicitly to a separate store (for example
  `aws_ssm_parameter`, `aws_s3_object`, DNS records, Consul keys or a Kubernetes config
  map) so access controls differ from those on state snapshots.

## Checked
Date: 2026-11-07
Read in full: "The terraform_remote_state Data Source" and "try Function".
Confirmed: arguments, `defaults` wording, `outputs`, root-outputs-only rule and passthrough example, security warning, `tfe_outputs` recommendation, explicit-store alternatives, `try` behaviour, recommendations and limits.
Removed (not on the pages): the sample "Unsupported attribute" error text and its cause list, the claim that `outputs` is the upstream merged over `defaults` with upstream keys winning, S3 example values, the `precondition` pattern, the advice to keep renamed outputs for one release, the OpenTofu angle, and the Verify steps.
Method: documentation only; no commands were run.
