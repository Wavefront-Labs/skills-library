---
id: computing-software.cloud-infrastructure-engineering.terraform.provider-blocks-in-terraform-stacks
name: provider-blocks-in-terraform-stacks
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, stack-providers, terraform-stacks, tfcomponent-hcl, provider-for-each, identity-token, component-providers]
level: practitioner
status: docs-checked
description: "Configure providers in Terraform Stacks: two-label provider blocks with a config block, for_each per region, OIDC identity tokens, passing providers to components, lock file."
sources:
  - https://developer.hashicorp.com/terraform/language/stacks/component/declare-providers
  - https://developer.hashicorp.com/terraform/language/stacks/deploy/authenticate
licence: Apache-2.0
version: 3
updated: 2026-11-17
---
# Provider blocks in stacks

In a Stack, providers are declared in a top-level `.tfcomponent.hcl` file and passed to each `component` block; modules sourced by components cannot declare their own providers.

## Differences from ordinary provider blocks
- Each `component` block accepts a top-level map of providers.
- Arguments are passed through a `config` block.
- The alias name is part of the block header: `provider "aws" "this"`.
- Providers support `for_each`.
- Every provider you define must also be listed in `required_providers`, so Terraform knows which version to download.

## Declare and configure
```hcl
# providers.tfcomponent.hcl
required_providers {
  aws = { source = "hashicorp/aws", version = "~> 5.7.0" }
}

provider "aws" "configurations" {
  for_each = var.regions                       # one provider configuration per region
  config {
    region = each.value
    assume_role_with_web_identity {
      role_arn           = var.role_arn
      web_identity_token = var.identity_token
    }
  }
}
```
The `for_each` form gives a configuration per region, addressed as `provider.aws.configurations[each.value]`.

## Pass providers to components
```hcl
# components.tfcomponent.hcl
component "s3" {
  for_each = var.regions
  source   = "./s3"
  inputs   = { region = each.value }
  providers = {
    aws    = provider.aws.configurations[each.value]
    random = provider.random.this
  }
}
```
(`provider.random.this` assumes a `random` provider block with alias `this` declared as above.)

## Authentication with OIDC
The docs recommend OIDC over static credentials. The `identity_token` block in the deployment file creates a workload identity token (JWT); the deployment passes it, with the role ARN, as inputs.
```hcl
# deployments.tfdeploy.hcl
identity_token "aws" {
  audience = ["aws.workload.identity"]
}
deployment "development" {
  inputs = {
    role_arn       = "<YOUR_ROLE_ARN>"
    identity_token = identity_token.aws.jwt
  }
}
```
```hcl
# variables.tfcomponent.hcl
variable "role_arn"       { type = string }
variable "identity_token" {
  type      = string
  ephemeral = true
}
```
The cloud side needs a trust relationship. The AWS example on the page creates an OpenID Connect provider with URL `https://app.terraform.io` and client ID `aws.workload.identity`, and a role whose trust policy requires `app.terraform.io:aud` to equal `aws.workload.identity` and `app.terraform.io:sub` to match a pattern such as `organization:<org>:project:<project>:stack:<stack>:*`. Widen or narrow the pattern to control which organizations, projects, stacks, deployments or operations may assume the role; the page's "Configure trust" reference defines the exact claim format and was not opened.

Alternative: a `store "varset"` block in the deployment file reads credentials from an HCP Terraform variable set, referenced as `store.varset.<STORE_NAME>.<VARIABLE_NAME>`. Values are not saved to deployment state by default; the `stable` keyword persists those that must be.

## Lock file
A Stack cannot run without a provider lock file. `terraform stacks init` downloads the providers listed in `required_providers` and creates `.terraform.lock.hcl`; after changing provider versions run `terraform stacks init -upgrade`. Only certain provider versions support deferred changes (for example Kubernetes provider 2.32.0 or higher), so check the registry page for the provider.

## Checked
Date: 2026-11-07. Read in full: "Declare providers" (now at stacks/component/declare-providers; the old create/declare-providers URL redirects there) and "Authenticate a Stack". Corrections made: file extension is `.tfcomponent.hcl`, not `.tfstack.hcl`; the lock file command is `terraform stacks init` (`-upgrade`), not `providers-lock`; variables live in `variables.tfcomponent.hcl`. Removed because neither page states them: the Azure `client_id_file`/`oidc_token` and GCP patterns, the `deployment:prod:operation:*` subject string, "every nested-module provider must be passed", the `removed`-block advice for dropping a region, `terraform stacks validate`, and the Verify list. Dropped the stacks/create/components source (404). Example version constraint now matches the page (`~> 5.7.0`).
Method: documentation only; no commands were run.
