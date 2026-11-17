---
id: computing-software.devops-ci-cd.packer.source-block
name: source-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [source, builder, hcl2, reuse, block-source]
level: practitioner
status: docs-checked
description: "Define reusable builder configuration with a top-level source block and reference it from build blocks."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/source/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

A `source` block defines reusable builder configuration. It has two labels: the builder type and a name.

```hcl
source "happycloud" "foo" {
  # builder options
}
```

One `source.happycloud.foo` exists at top level but can be used by many builds. A build references it two ways:

```hcl
build {
  sources = ["source.happycloud.example", "source.happycloud.foo"]
}
```

or with a build-level `source` block that sets extra fields:

```hcl
build {
  source "source.happycloud.example" {
    image_name = "build_specific_field"
  }
}
```

Fields cannot be overridden. If `image_name` is set in the top-level source it may not be set again in the build-level block; each field may be defined only once.

A build-level `source` may also set `name`, which renames it for `override` and the `source.name` variable.

Provisioners and post-processors can read `source.name` and `source.type`.

## Checked
2026-11-03. Confirmed against the source block page (labels, reuse across builds, `sources` and build-level `source`, fields cannot be overridden, `source.name` / `source.type`) and the provisioner block page (rename and override key). Removed the required_plugins claim, `-only`/`-except` renaming and a closing tip.
Method: documentation only; no commands were run.
