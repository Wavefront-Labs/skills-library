---
id: computing-software.cloud-infrastructure-engineering.terraform.aws-provider-default-tags-and-ignore-tags
name: aws-provider-default-tags-and-ignore-tags
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, default-tags, ignore-tags, aws-provider, tagging, tags-all]
level: practitioner
status: docs-checked
description: "Configure AWS provider default_tags and ignore_tags: tags_all, resource-level tags, the autoscaling group exception, aliased providers and tag-resource conflicts."
sources: ["https://github.com/hashicorp/terraform-provider-aws/blob/main/website/docs/guides/resource-tagging.html.markdown"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# AWS `default_tags` and `ignore_tags`

```hcl
provider "aws" {
  region = "eu-west-1"
  default_tags {
    tags = {
      Environment = var.env
      Service     = "payments"
      ManagedBy   = "terraform"
    }
  }
  ignore_tags {
    keys         = ["LastScanned"]
    key_prefixes = ["kubernetes.io/"]
  }
}
```

## How it works (resource tagging guide)
- `default_tags` goes in the `provider "aws"` block and applies to all resources that support `tags`, except
  `aws_autoscaling_group`. Resource-level `tags` are still allowed and are combined with the provider defaults.
- `tags_all` is a read-only attribute showing all tags on a resource, including provider defaults
  (for example `aws_vpc.example.tags_all`). Do not set it in configuration.
- `ignore_tags` is configured in the provider block. `keys` ignores tags with the listed keys and `key_prefixes`
  ignores tags whose keys start with the listed prefixes; they can be combined, and apply across resources under
  that provider (unlike `lifecycle` `ignore_changes`, which is per resource).
- With multiple provider instances (aliases), add the configuration to each provider that needs it.

## Gotchas
- Not every AWS resource supports tags; check each resource's `tags` argument in its documentation.
- `aws_autoscaling_group` is excluded from `default_tags`; tag it through its own tagging arguments.
- Tag keys beginning with `aws:` are managed by AWS and generally cannot be edited or deleted.
- Do not combine individual tag resources (such as `aws_ec2_tag`) with the parent resource's `tags` for the same
  object: it causes perpetual differences.

## Checked
2026-11-01. Confirmed on the provider's resource-tagging guide (source markdown in hashicorp/terraform-provider-aws):
default_tags, tags_all, ignore_tags keys and key_prefixes, autoscaling group exclusion, per-provider configuration,
`aws:` prefix and tag-resource caveat. Removed: merge precedence claim, launch-template and EBS propagation notes,
provider-version fix claims, timestamp and unknown-value pitfalls, tag policy remark, verify steps. The registry
pages cited before are JavaScript stubs and could not be read.
Method: documentation only; no commands were run.
