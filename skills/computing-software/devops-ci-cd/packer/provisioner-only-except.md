---
id: computing-software.devops-ci-cd.packer.provisioner-only-except
name: provisioner-only-except
category: computing-software
field: devops-ci-cd
product: packer
tags: [provisioner-only, provisioner-except, sources, filter, block-provisioner]
level: practitioner
status: docs-checked
description: "Run a provisioner on specific sources using only and except, which match source names rather than build names."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/provisioner/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`only` and `except` on a provisioner (or post-processor) restrict it to particular sources.

```hcl
build {
  sources = ["source.amazon-ebs.first-example", "source.amazon-ebs.second-example"]
  provisioner "shell" {
    only   = ["amazon-ebs.first-example"]
    inline = ["echo only for the first source"]
  }
  provisioner "shell" {
    inline = ["echo runs for all sources"]
  }
}
```

Rules from the docs:

- Names omit the `source.` prefix: use `amazon-ebs.first-example`.
- Values are source names (type.name), not builder types and not build names.
- `only` runs the provisioner only on listed sources; `except` runs it on everything else.
- The command-line `-only` and `-except` flags are different: they match build names such as `my_build.amazon-ebs.first-example`, while inside a provisioner the match is on the source name `amazon-ebs.third-example`.

For per-source differences in settings rather than skipping, use `override`.

## Checked
2026-11-03. Confirmed against the provisioner block page: `only` / `except` semantics, names without the `source.` prefix, source names rather than builder or build names, and the difference from command-line matching. Removed the unsourced renaming and validate advice.
Method: documentation only; no commands were run.
