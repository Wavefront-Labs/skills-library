---
id: computing-software.cloud-infrastructure-engineering.terraform.ignore-changes-on-tags-and-map-keys
name: ignore-changes-on-tags-and-map-keys
category: computing-software
field: cloud-infrastructure-engineering
product: terraform
tags: [terraform, opentofu, ignore-changes-tags, ignore-changes, tags, drift]
level: practitioner
status: docs-checked
description: "Ignore only specific tag keys or map entries with ignore_changes index syntax, and avoid hiding real drift from externally applied tags."
sources: ["https://developer.hashicorp.com/terraform/language/meta-arguments/lifecycle"]
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

# `ignore_changes` on tags

## Ignore specific keys, not the whole map
```hcl
lifecycle {
  ignore_changes = [
    tags["LastScanned"],
    tags["aws:cloudformation:stack-name"],
    labels["goog-managed-by"],
  ]
}
```
- Use `ignore_changes` when another process manages some of a resource's settings, or when a value is set at creation and should not be updated later. Terraform skips the listed attributes when planning an update.
- Individual map or list elements can be targeted with index notation (the docs show `tags["Name"]` and `list[0]`). Prefer that over ignoring `tags` entirely, which hides real drift on every tag.
- Only attributes defined by the resource type can be ignored, `ignore_changes` cannot reference itself or other meta-arguments, and it works only in `resource` blocks.
- Lifecycle settings accept literal values only, because they are processed before arbitrary expressions can be evaluated.
- The named attributes are considered when planning a create; they are ignored when planning an update. So a change you make in config to an ignored key will not be applied on an existing resource.
- `ignore_changes = all` ignores every attribute: Terraform can still create and destroy the object but never proposes updates.

## Gotchas
- Keys with special characters need quoting inside the index: `tags["aws:cloudformation:stack-name"]`.
- For provider-level tag handling (the AWS provider's `default_tags`, `tags_all` and `ignore_tags`), read the provider's resource-tagging guide for your provider version; those details are not covered here.

## Verify
- [ ] Two plans after an external tagger runs show no diff for the ignored keys.
- [ ] Changing a non-ignored tag in config still produces a plan diff.

## Checked
Method: docs-only read of cited pages, 2026-11-08
Confirmed on the Terraform lifecycle meta-argument page: purpose, index notation, `all`, create versus update, restrictions. Removed: the table of tag sources, AWS `ignore_tags` and `tags_all` guidance, and the claim about state refresh (the AWS registry guide page returned no readable content, and the lifecycle page does not cover them).
