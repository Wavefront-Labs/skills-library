---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-configuration-depending-on-resources
name: provider-configuration-depending-on-resources
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, provider-dependency, provider-configuration, unknown-provider-config, two-stage-apply, kubernetes-provider]
level: practitioner
status: docs-checked
description: "Provider blocks may only use values known before apply; avoid configuring a provider from a resource in the same run (cluster then in-cluster resources) by splitting stages."
sources:
  - https://developer.hashicorp.com/terraform/language/providers/configuration
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Provider configuration depending on resources

## What the docs say
The provider block reference states you can use expressions to configure provider arguments, but you can only reference
values that Terraform knows before it applies your configuration. You can reference input variables and arguments you
set directly in the configuration, but you cannot reference computed resource attributes such as
`google.web.public_ip`. Other points from the same page:
- Define provider configurations in the root module. Child modules receive their provider configurations from their
  parents, so HashiCorp strongly recommends against `provider` blocks in child modules.
- Without an explicit block, Terraform creates an empty default configuration; if the provider has required arguments
  that is an error.
- Many providers read credentials from environment variables or other alternate sources; see the provider's own docs.

## The classic trap
Configuring a provider from attributes of a resource that the same run creates (for example a Kubernetes or Helm
provider whose endpoint comes from a cluster resource in the same root module) means the provider arguments depend on
computed attributes. That is the pattern the docs rule out. The cluster and what is deployed inside it should not be
planned as one dependency graph through the provider block.

## Fix: split into stages
Create the endpoint in one root module (its own state) and configure the second provider in another root module that
looks the endpoint up with data sources or input variables:
```hcl
# second root module: cluster already exists
variable "cluster_name" { type = string }

data "<CLUSTER_DATA_SOURCE_TYPE>" "this" {
  name = var.cluster_name
}

provider "kubernetes" {
  host = data.<CLUSTER_DATA_SOURCE_TYPE>.this.<ENDPOINT_ATTRIBUTE>
  # credentials arguments per the provider's documentation
}
```
Take the data source type, attribute and authentication arguments from your cloud provider's and the Kubernetes
provider's documentation; they are not covered by the Terraform provider-block page.

Other options: a Terraform Stacks configuration (components deployed with `.tfdeploy.hcl` deployments) for one
orchestrated flow, or a GitOps tool for workloads after Terraform creates the cluster. Check current Stacks docs for
how they sequence dependent components.

## Same issue elsewhere
Any provider configured from something another resource creates (database, secrets store, Helm, SaaS workspace) has
the same constraint: separate the stage that creates the endpoint from the stage that configures inside it.

## Verify
- [ ] No `provider` block references a `resource` address or other computed attribute from the same root module.
- [ ] A change to the infrastructure root does not plan changes to in-cluster resources.

## Checked
Confirmed 2026-11-08 against the Terraform provider block reference: values must be known before apply, computed
attributes cannot be referenced, root-module provider placement, empty default configuration. The Stacks deploy
configuration page was read but does not describe deferred changes. Removed: provider-specific failure messages and
defaults, cycle error text, destroy behaviour, the EKS auth examples and 15-minute token expiry, the `-target`
workaround, deferred-changes claims for Stacks, exec-auth advice and the `grep` verify step (none on cited pages).
Method: docs-only read of cited pages, 2026-11-08
