---
id: computing-software.devops-ci-cd.packer.build-only-except
name: build-only-except
category: computing-software
field: devops-ci-cd
product: packer
tags: [only, except, filter, build-names, cmd-build, hcl-build]
level: practitioner
status: docs-checked
description: "Select builds with -only and -except, including how HCL2 names are formed from source blocks."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/build/"
  - "https://developer.hashicorp.com/packer/docs/templates/hcl_templates/blocks/build/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`-only` runs just the named builds and `-except` runs everything but the named builds. Both take comma-separated names and accept glob patterns such as `*.second-example`.

How names are formed:

- In HCL2 templates the name is the source block's name label, so `source "null" "second-example"` in an unnamed build is `null.second-example`.
- If the `build` block has a `name`, it prefixes the source: `a.null.second-example`.
- An in-build `source` block may add a `name` option, which replaces the label.
- In legacy JSON templates names default to the builder type (`docker`, `amazon-ebs`) unless a `name` attribute is set.

```bash
packer build -only "*.second-example" ./folder
packer build -except=checksum mytemplate.pkr.hcl
```

The docs point out a limit: matching a named build block on its own is not yet possible, so `a.*` matches nothing.

`-except` also applies to post-processors, by their `name`, which defaults to the type. Any post-processor after a skipped one will not run. `-only` does not work for post-processors; use `only = [...]` inside the template instead.

## Checked
2026-11-03. Confirmed against the build block page (naming, `-only "*.second-example"` example, `a.*` matching nothing), the build command page (HCL2 and JSON naming, in-build `name` option) and the post-processor block page (`-except` by name, `-only` not working).
Method: documentation only; no commands were run.
