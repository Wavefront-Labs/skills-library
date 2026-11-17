---
id: computing-software.cloud-infrastructure-engineering.terraform.import-by-resource-identity
name: import-by-resource-identity
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, import-identity, identity-attribute, resource-identity, import-block, provider-schema]
level: practitioner
status: docs-checked
description: "Import with the import block identity argument (Terraform 1.12+) instead of an opaque id string: what resource identity is, the id/identity rules and required or optional keys."
sources: ["https://developer.hashicorp.com/terraform/language/import", "https://developer.hashicorp.com/terraform/language/block/import", "https://developer.hashicorp.com/terraform/plugin/framework/resources/identity"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# Importing by resource identity

Terraform identifies a resource either by the ID the cloud provider assigns or by a set
of specific attributes the provider defines. In configuration you refer to it with the
`id` or the `identity` argument of an `import` block. Resource identity is supported in
Terraform 1.12 and later.

## What an identity is
A data object, determined by the provider and stored alongside the resource state. It
must map to at most one remote object per provider, must let the provider decide whether
that object exists during import, and must not change over the object's life (unless the
provider upgrades the identity schema).

The language overview's example: for `s3_bucket` in the AWS provider, the identity is
`account_id`, `bucket` and `region`; for `aws_instance` you use the `id` attribute. Your
provider's documentation says how to reference a resource's identity.

## Syntax
```hcl
import {
  to = examplecloud_thing.test
  identity = {
    id     = "id-123"      # required for import
    region = "us-east-1"   # optional for import
  }
}
```
- `identity` is an object of key-value pairs; keys and values depend on the resource type
  and provider.
- `id` and `identity` cannot be used in the same block. In the plugin framework docs,
  supplying both or neither is a validation error.
- `id` must be a string, or an expression resolving to one, known during plan.
- `to` must match the address of an existing `resource` block.

## Required and optional keys
Provider authors mark each identity attribute `RequiredForImport` (you must set a known,
non-null value or Terraform raises an error) or `OptionalForImport` (set a known value or
null; the provider may default it, for example from provider configuration). Exactly one
of the two is expected per attribute.

## ID fallback
A resource that defines an identity can still be imported by ID with `terraform import
examplecloud_thing.test id-123` or an `import` block with `id`. Providers must keep
supporting the ID form if identity data is absent, but a provider that only supports
Terraform 1.12+ may reject IDs with an error diagnostic. If a provider does not
document an identity for a resource, use `id`.

## Checked
Date: 2026-11-07
Read in full: Import resources overview (language/import), import block reference (language/block/import), and Resource Identity in the plugin framework docs (plugin/framework/resources/identity).
Confirmed: 1.12 support statement; identity definition and properties; id/identity exclusivity; the S3 bucket and aws_instance examples; required versus optional import behaviour; ID fallback and provider behaviour; `to` and `id` rules.
Removed: the `terraform providers schema -json` jq command and `resource_identity_schemas` key (the JSON format page has no identity section), "clear validation errors instead of Cannot import non-existent remote object", `terraform show -json` and `terraform query` claims, the OpenTofu and HCP Terraform workspace version notes, the cross-region `provider = aws.use1` advice, the S3 `identity = { bucket = ... }` example (the page lists three identity attributes for S3), and the Verify checklist.
Not opened: the provider-specific import documentation on the registry.
Method: documentation only; no commands were run.
