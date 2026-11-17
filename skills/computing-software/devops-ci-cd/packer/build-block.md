---
id: computing-software.devops-ci-cd.packer.build-block
name: build-block
category: computing-software
field: devops-ci-cd
product: packer
tags: [build-block, sources, name, hcl2, block-build]
level: practitioner
status: docs-checked
description: "The build block ties sources to provisioners and post-processors, and its name prefixes log lines and -only matching."
sources:
  - https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

The `build` block says which builders to run, how to provision them, and what post-processing to do with the artifacts.

```hcl
build {
  name = "buildname"
  sources = ["source.amazon-ebs.example-1"]
  source "source.amazon-ebs.example-2" {
    output = "different value"
    name   = "differentname"
  }
  provisioner "shell" {
    scripts = fileset(".", "scripts/{install,secure}.sh")
  }
  post-processor "shell-local" {
    inline = ["echo ${source.type}.${source.name}"]
  }
}
```

Choose sources in either of two ways: the `sources` list of references, or build-level `source` blocks that let you set fields. Fields cannot be overwritten: you cannot set `output` both in the top-level source block and in the build-level one.

The optional `name` prefixes log lines. With `name = "a"` you see `Build 'a.null.first-example' finished.`; an unnamed block prints `Build 'null.second-example' finished.`. The name appears in the artifact list at the end too.

Several `build` blocks can live in one folder (the page's example has two). `-only` and `-except` match a source's `type.name`, so `-only "*.second-example"` runs that source in every build block that references it. Build names are not yet matchable, so `a.*` matches nothing.

## Checked

Method: documentation only; no commands were run. Checked 2026-11-09 against the Packer 1.15 `build` block reference and its example partial. Removed as not on the page: "each is independent", "provisioners run in the order written" and "post-processor blocks run after each source finishes provisioning".
