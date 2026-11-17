---
id: computing-software.devops-ci-cd.packer.provisioner-override
name: provisioner-override
category: computing-software
field: devops-ci-cd
product: packer
tags: [override, per-source, build-specific, provisioner, block-provisioner]
level: advanced
status: docs-checked
description: "Merge build-specific settings into a provisioner for one source with the override map."
sources:
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/provisioner/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`override` is an attribute map keyed by source name. Each value is a map of provisioner settings that is merged into the provisioner's default configuration for that source.

```hcl
build {
  sources = ["source.null.example2", "source.null.example3"]
  source "source.null.example1" {
    name = "renamed"
  }
  provisioner "shell-local" {
    inline = ["echo not overridden"]
    override = {
      example3 = { inline = ["echo overrides for example3"] }
      renamed  = { inline = ["echo overrides for renamed"] }
    }
  }
}
```

Use it when a script has to run differently per platform before images converge. The docs' example: an EC2 AMI source may already have a user with admin privileges while a VMware machine does not, so the shell command may need to be invoked differently on each.

Key by the source's name: `example3` for a plain source, `renamed` for one given a `name` inside the build. Settings not mentioned in the override keep their default values.

## Checked
2026-11-03. Confirmed against the provisioner block page: `override` is keyed by source name, values are merged into the default configuration, the EC2 versus VMware rationale and the `renamed` source example. Removed a legacy JSON claim the page does not make.
Method: documentation only; no commands were run.
