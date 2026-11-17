---
id: computing-software.cloud-infrastructure-engineering.terraform.state-identities-listing
name: state-identities-listing
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, state-identities, resource-identity, import-identity, state-inspection]
level: practitioner
status: docs-checked
description: "List resource identities stored in state with terraform state identities -json, filter by address or id, and know what resource identity is (Terraform 1.12+)."
sources: ["https://developer.hashicorp.com/terraform/cli/commands/state/identities", "https://developer.hashicorp.com/terraform/language/import#import-by-identity", "https://developer.hashicorp.com/terraform/plugin/framework/resources/identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `terraform state identities`

## What resource identity is
A resource identity is a data object, determined by the provider, stored alongside the resource state to uniquely
identify a remote object. It is supported in Terraform 1.12 and later. Per the plugin framework docs it must map to at
most one remote object per provider, must let the provider find the object during import, and must not change over the
object's lifecycle (until the provider upgrades the identity schema).

Terraform identifies a resource either by the ID the cloud provider assigns or by a set of attributes the provider
defines. In configuration you reference it with the `id` or `identity` attribute. Example from the import overview: the
AWS provider's `s3_bucket` identity is made of `account_id`, `bucket` and `region`, while an `aws_instance` is
referenced with `id`. See your provider's docs for how each resource is identified, and the `import` block reference for
the identity syntax.

## Listing identities
```bash
terraform state identities -json
terraform state identities -json aws_instance.example
terraform state identities -json module.example
terraform state identities -id=<ID> -json
```
Usage: `terraform state identities [options] -json [address...]`. It prints a JSON object mapping each resource instance
address to its identity object.
- `-json` is required.
- `-state=path` reads a state file; by default Terraform uses the state of the currently selected workspace.
- `-id=id` keeps only instances whose `id` attribute equals the string.
- Addresses may be resource or module addresses (`aws_instance.example`, `aws_instance.example[0]`, `module.example`,
  `module.example[0]`, `module.example.module.child`, `module.example.aws_instance.example`). A module address lists
  resources in that module and its submodules. With no address, all instances are listed.
- A resource with no identity is not listed. A filter address that does not exist in state is an error.

## Uses
- Inventory: the identity attributes per resource, without parsing provider ID strings.
- Feeding identity-based imports: read the identity values from the old state when re-importing into a new root (write
  the `import` blocks using the identity syntax in the import block reference).

## Gotchas
- Not every resource type has an identity yet; missing entries are expected.
- Resource identity needs Terraform 1.12 or later. OpenTofu: check its own documentation (not covered here).

## Checked

Checked 2026-11-08 against the Terraform `terraform state identities` command page, the Import resources overview and the
plugin framework Resource Identity page: usage, flags, address forms, filter and error behaviour, identity properties,
the 1.12 requirement and the S3 bucket identity attributes. Removed (not stated on the fetched pages): provider support
list, the `jq` import-block generator and the `import { identity = ... }` syntax, the refresh/plan population claim and
the OpenTofu `state --help` remark.

Method: documentation only; no commands were run.
