---
id: computing-software.cloud-infrastructure-engineering.terraform.common-tags-pattern-with-merge
name: common-tags-pattern-with-merge
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, common-tags, locals, merge-function, tagging]
level: practitioner
status: verified
description: "Apply a consistent tag/label set across resources with a common_tags local and merge(), compare with AWS default_tags, and avoid perpetual tag diffs."
sources: ["https://developer.hashicorp.com/terraform/language/functions/merge", "https://registry.terraform.io/providers/hashicorp/aws/latest/docs/guides/resource-tagging", "https://developer.hashicorp.com/terraform/language/values/locals"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `common_tags` pattern

```hcl
locals {
  common_tags = {
    Environment = var.env
    Service     = "payments"
    Owner       = "team-payments"
    ManagedBy   = "terraform"
    Repo        = "github.com/corp/payments-infra"
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = "payments-${var.env}-logs"
  tags   = merge(local.common_tags, { Name = "payments-${var.env}-logs", DataClass = "internal" })
}
```
Later arguments to `merge` win, so per-resource tags can override common ones.

## Modules
Pass tags in, merge inside, never hard-code inside the module:
```hcl
variable "tags" {
  type    = map(string)
  default = {}
}
resource "aws_sqs_queue" "q" {
  name = var.name
  tags = merge(var.tags, { Name = var.name })
}
```

## AWS: prefer `default_tags` for the common part
```hcl
provider "aws" {
  default_tags { tags = local.common_tags }
}
```
Then resources only set specific tags. The AWS provider's tagging guide says this works
for all resources that support `tags` except `aws_autoscaling_group`, and that not all AWS
resources support tagging at all; `merge` (or the ASG `tag` blocks) is still needed there.
The `azurerm` provider docs index lists no provider-level default tags, so use the local
pattern there. The Google provider has `default_labels` in its provider block (provider
reference guide), and per-resource `labels = merge(local.common_labels, {...})` still
works; label keys and values must be lowercase.

## Pitfalls
- Values that change every run (`timestamp()` as `CreatedAt`) cause perpetual diffs;
  use `ignore_changes = [tags["CreatedAt"]]` (the same index syntax works on any map
  argument, e.g. `input["CreatedAt"]` on `terraform_data`) or drop such tags.
- Tag value limits: AWS 256 characters (keys 128), Azure 256 (names 512; 128 on storage
  accounts), GCP labels 63 characters of lowercase letters, digits, `_` and `-`.
- `merge` copies keys left to right, so a per-resource tag with the same key as a common
  tag overrides it silently; keep resource-specific keys distinct from the common set.

## Verify
- [ ] Tag policy/scan shows required tags on every resource.
- [ ] Two consecutive plans show no tag-only diffs.

## Checked
- Terraform 1.17.0, `terraform_data`: `merge(local.common_tags, {...})` let the later map win (`Owner = "override"`) and `merge({a=1,b=1},{b=2})` gave `b = 2`; a `timestamp()` tag produced a perpetual in-place diff on the second plan, while `ignore_changes = [input["CreatedAt"]]` gave `No changes`.
- Provider facts: `default_tags` and `ignore_tags` appear in the aws provider tagging guide (hashicorp/terraform-provider-aws docs source), which lists `aws_autoscaling_group` as the exception; `aws_s3_bucket.bucket` and `aws_sqs_queue.name` exist in the resource docs; tag limits were read on the AWS Tag Editor best-practices page (value max 256), Microsoft Learn tag-resources (value 256) and Google Cloud labels overview (63, lowercase keys and values). The old claim that duplicate keys in `default_tags` and resource `tags` caused diffs in older provider versions was removed (no source found).
- Correction found while checking: the Google provider reference documents `default_labels` (the old text said Google had no default tags); the azurerm docs index (hashicorp/terraform-provider-azurerm) has no `default_tags` entry.
