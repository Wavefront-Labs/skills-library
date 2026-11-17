---
id: computing-software.cloud-infrastructure-engineering.terraform.terraform-stacks-publish-output-and-upstream-input
name: terraform-stacks-publish-output-and-upstream-input
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, publish-output, upstream-input, linked-stacks, terraform-stacks, cross-stack-dependencies, tfdeploy-hcl]
level: practitioner
status: docs-checked
description: "Link Terraform Stacks together with publish_output and upstream_input blocks: exposing values, consuming them in another stack, automatic downstream plans and design limits."
sources:
  - https://developer.hashicorp.com/terraform/language/stacks/deploy/pass-data
  - https://developer.hashicorp.com/terraform/language/block/stack/tfdeploy/publish_output
  - https://developer.hashicorp.com/terraform/language/block/stack/tfdeploy/upstream_input
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# publish_output and upstream_input

Linked stacks let one stack (e.g. networking) publish values that another stack (e.g. applications) consumes, for Stacks that do not share a provisioning lifecycle.

Both blocks require Terraform 1.10.0-alpha20241009 or higher.

## Producer stack
First expose a value from the stack with an `output` block in the component configuration, then publish it from the deployment configuration:
```hcl
# components.tfcomponent.hcl
output "vpc_id" {
  description = "The VPC ID of the networking Stack"
  type        = string
  value       = component.vpc.vpc_id
}
```
```hcl
# network.tfdeploy.hcl
publish_output "vpc_id_network" {
  description = "The networking Stack's VPC's ID."
  value       = deployment.network.vpc_id
}
deployment "network" {
  # ...
}
```
Reference a deployment output as `deployment.<DEPLOYMENT_NAME>.<OUTPUT_NAME>`. Each value you want to expose needs its own `publish_output` block; the label must be unique in the deployment file. `value` is required, `description` optional.

## Consumer stack
```hcl
# application.tfdeploy.hcl
upstream_input "network_stack" {
  type   = "stack"                       # the only supported type
  source = "app.terraform.io/<ORGANIZATION>/<PROJECT>/<STACK_NAME>"
}

deployment "application" {
  inputs = {
    vpc_id = upstream_input.network_stack.vpc_id_network
  }
}
```
Reference published outputs as `upstream_input.<LABEL>.<OUTPUT_NAME>`. Declare one `upstream_input` block per upstream stack.

## Behaviour and limits
- After the producer's deployment configuration is applied, HCP Terraform stores a snapshot of the published values. The producer must be applied before downstream stacks can reference them; if no snapshot exists the downstream run fails.
- When a published output value changes, HCP Terraform automatically triggers runs for downstream stacks that depend on it.
- Upstream and downstream stacks must be in the same project.
- A stack can link to up to 20 upstream stacks and expose values to up to 25 downstream stacks.
- To stop depending on an upstream stack: remove the `upstream_input` block and every reference to its outputs, then push and apply.

## Design guidance (authored advice, not from the docs)
- Publish stable, coarse identifiers (VPC ID, subnet IDs) rather than whole objects that change often, since every change triggers downstream runs.
- Treat published outputs as an API: add new outputs before removing old ones.

## Verify
- [ ] Consumer run shows inputs resolved from the producer; changing a published value triggers a downstream run.

## Checked

Method: docs-checked 2026-11-09 against the three cited pages (downloaded, converted to text and read in full for the relevant sections): pass-data guide, publish_output reference, upstream_input reference. Corrected file extension to .tfcomponent.hcl and same-project (not same-organisation) rule. Dropped unconfirmed claims: consumer read access, sensitive-value handling, cycle prevention, tfe_outputs alternative.
