---
id: computing-software.devops-ci-cd.packer.hcl2-upgrade-command
name: hcl2-upgrade-command
category: computing-software
field: devops-ci-cd
product: packer
tags: [hcl2-upgrade, migration, json, templates, cmd-hcl2upgrade]
level: practitioner
status: docs-checked
description: "Convert a JSON template or variables file to HCL2 with packer hcl2_upgrade and know what it transforms."
sources:
  - "https://developer.hashicorp.com/packer/docs/commands/hcl2_upgrade/"
licence: Apache-2.0
version: 3
updated: 2026-11-17
---

`packer hcl2_upgrade` transpiles a JSON template into formatted HCL2. It is marked beta in the docs, so review the output.

```bash
packer hcl2_upgrade my-template.json
# Successfully created my-template.json.pkr.hcl
```

Options:

- `-output-file` sets the output name; the default is the input name plus `.pkr.hcl`.
- `-with-annotations` adds comments describing each generated block.

Since v1.7.1 it can also upgrade a variables file: a JSON `variables` map becomes `variable` blocks, and names listed under `sensitive-variables` get `sensitive = true`.

Go template calls it converts:

- `{{ user `my_var` }}` becomes `${var.my_var}`
- `{{ env `my_var` }}` becomes `${var.my_var}`, since HCL2 reads environment variables through input variables
- `{{ timestamp }}` becomes `${local.timestamp}`, and a local is created in every generated file
- `{{ build `ID` }}` becomes `${build.ID}`

Other calls stay as Go template calls. When a conversion fails, the block is emitted untransformed with the error in a comment. HCL2 variables cannot use functions or other variables, so user variables built from other user variables need locals (older versions up to 1.7.0 do not convert them to locals automatically).

## Checked
2026-11-03. Confirmed against the packer hcl2_upgrade command page: beta status, usage output, the v1.7.1 variables file upgrade, the four Go template conversions, failure behaviour, both options and the locals note for v1.7.0 and lower.
Method: documentation only; no commands were run.
