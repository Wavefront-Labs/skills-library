---
id: computing-software.cloud-infrastructure-engineering.terraform.for-each-over-sets-and-module-for-each
name: for-each-over-sets-and-module-for-each
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, for-each, toset-for-each, for-each-set, module-for-each, module-count, each-value]
level: practitioner
status: verified
description: "Iterate resources over toset() lists and instantiate modules with for_each/count: keys, each.value, referencing module instances, and migrating from count."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/for_each", "https://developer.hashicorp.com/terraform/language/meta-arguments/count", "https://developer.hashicorp.com/terraform/language/modules/syntax"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `for_each` over sets, and on modules

## Over a list of strings
```hcl
variable "buckets" { type = list(string) }        # ["logs", "assets"]

resource "aws_s3_bucket" "this" {
  for_each = toset(var.buckets)
  bucket   = "acme-${each.key}"                   # each.key == each.value for sets
}
```
- `for_each` accepts maps or **sets of strings**; a list errors (`must be a map, or set of
  strings, and you have provided a value of type list of string`) - wrap in `toset()`.
- `toset` removes duplicates and ordering; keys are the strings, so removing one
  element touches only that instance (unlike `count`, which shifts indices).
- Sets of objects are not allowed (`"for_each" supports maps and sets of strings, but you
  have provided a set containing type object`); convert to a map:
  `{ for o in var.list : o.name => o }`.

## Modules
```hcl
module "service" {
  source   = "./modules/service"
  for_each = var.services                         # map(object)
  name     = each.key
  cpu      = each.value.cpu
}

output "service_urls" {
  value = { for k, m in module.service : k => m.url }
}
```
- Address: `module.service["api"]`; reference one: `module.service["api"].url`.
- `count` on modules is the toggle form: `count = var.enabled ? 1 : 0`, referenced as
  `module.x[0]` or `one(module.x[*].url)`.
- Supported since Terraform 0.13 (0.13 changelog). A module containing its own `provider`
  configuration blocks cannot be used with `for_each`, `count` or `depends_on` (`Error: Module
  is incompatible with count, for_each, and depends_on`; see legacy-provider skill).

## From count to for_each
Index → key mapping with `moved` blocks (see moved count-to-for-each skill).

## Gotchas
- `for_each` keys must be known at plan (no resource IDs) and non-sensitive.
- `each` is only available inside the block; outputs must iterate the collection.
- Changing a key = destroy + create of that instance.

## Verify
- [ ] Removing one element from `var.buckets` plans exactly one destroy (`["logs","assets","logs"]` to `["logs"]` planned only `this["assets"]` destroyed; duplicates collapse).
- [ ] `terraform state list module.service` shows `module.service["<key>"]` addresses.

## Checked
- Terraform 1.17.0, `terraform_data` for the bucket resource and a local `modules/service`: `for_each = var.buckets` on a list gave the list error and `toset([{ name = "a" }])` the object-set error (texts quoted); `toset(["logs","assets","logs"])` created two instances with `each.key == each.value`; `module.service["api"]`/`["web"]` addresses and `state list module.service` matched; `{ for k, m in module.service : k => m.url }` and `module.service["api"].url` worked; `count = 1` on a module with `one(module.cm[*].url)` worked; a module with its own non-empty `provider "tls"` block gave `Module is incompatible with count, for_each, and depends_on`; the module count/for_each feature note is from the 0.13 changelog.
- AWS `aws_s3_bucket.bucket` was checked against the provider docs source.
